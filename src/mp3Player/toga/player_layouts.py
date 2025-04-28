from __future__ import annotations

import dataclasses
import logging
from enum import Enum
from pathlib import Path

import toga
from pyMOSF.config import Dict
from pyMOSF.toga import TogaComponent, TogaMultiLayoutApp, TogaStackedLayout
from toga.sources import Row as Source_ROW
from toga.style import Pack
from toga.style.pack import CENTER, COLUMN, ROW  # type: ignore

from mp3Player.icons import Icons
from mp3Player.services import PlayerStatus, PlayingThreadGlobals, ProgressThread, mp3

log = logging.getLogger(__name__)


class AudioState(int, Enum):
    LOADING = 0
    STOP = 1
    PLAYING = 2
    PAUSED = 3
    ADDING = 4
    REMOVING = 5
    SELECTING = 6


@dataclasses.dataclass
class Audio:
    @classmethod
    def create(cls):
        return cls(track=Dict({"name": "",
                               "length": "",
                               "path": ""}),
                   playlist_name="",
                   index=-1)

    @staticmethod
    def empty_track():
        return Dict({"name": "",
                     "length": "",
                     "path": ""})

    track: Dict
    playlist_name: str
    index: int

    CHAR_SIZE = 10

    def track_name_trimmed(self, max_width):
        char_nums = int(max_width / self.CHAR_SIZE) - 3

        if char_nums <= len(self.track.name):
            return self.track.name[:char_nums] + "..."
        else:
            return self.track.name

    def is_empty_track(self):
        return self.track.name == ""


class PlayerDeckComponent(TogaComponent):
    def __init__(self, layout: TogaStackedLayout, **kwargs) -> None:
        icons = Icons.load()
        icon_style = Pack(width=50,
                          height=48,
                          padding_left=10,
                          padding_bottom=4)  # , background_color="#666666")
        buttons_box = toga.Box(style=Pack(direction=ROW, alignment=CENTER),
                               children=[
                                   toga.Button(icon=icons.previous,
                                               on_press=self.previous,
                                               style=icon_style),
            toga.Button(icon=icons.play,
                                       on_press=self.play,
                                       style=icon_style),
            toga.Button(icon=icons.stop,
                                       on_press=self.stop,
                                       style=icon_style),
            toga.Button(icon=icons.next,
                                       on_press=self.next,
                                       style=icon_style),
        ])
        playing_track_box = toga.Box(style=Pack(direction=ROW, alignment=CENTER),
                                     children=[
            toga.Label("", style=Pack(padding_bottom=15,
                                      color="#119900", alignment=CENTER)),
        ])
        playing_progress_box = toga.Box(style=Pack(direction=ROW, alignment=CENTER),
                                        children=[
            toga.Label("00:00:00", style=Pack(padding_right=5, font_size=10,
                                              color="#119900", alignment=CENTER)),
            toga.ProgressBar(max=100,
                             value=0,
                             style=Pack(width=120, padding=5,)),
            toga.Label("00:00:00", style=Pack(padding_left=5, font_size=10,
                                              color="#119900", alignment=CENTER)),
        ])

        super().__init__(layout, style=Pack(
            direction=ROW, alignment=CENTER, padding=1),
            children=[toga.Box(style=Pack(direction=COLUMN, alignment=CENTER),
                               children=[
                                   buttons_box,
                                   playing_progress_box,
                                   playing_track_box,
            ],),
        ])
        self.btn_play = buttons_box.children[1]
        self.btn_stop = buttons_box.children[2]
        self.lb_playing_track = playing_track_box.children[0]
        self.lb_playing_left = playing_progress_box.children[0]
        self.playing_progress = playing_progress_box.children[1]
        self.lb_playing_remain = playing_progress_box.children[2]
        #
        self.audio_state: AudioState = AudioState.STOP

    def on_ios_config(self):
        from mp3Player.services.players_ios import RemoteCommandCenter
        center = RemoteCommandCenter.shared_instance()
        # None will pass as a widget
        center.play_command(self.play, None)
        center.pause_command(self.play, None)
        center.stop_command(self.stop, None)
        center.next_command(self.next, None)
        center.previous_command(self.previous, None)

    def on_ipados_config(self):
        from mp3Player.services.players_ios import RemoteCommandCenter
        center = RemoteCommandCenter.shared_instance()
        # None will pass as a widget
        center.play_command(self.play, None)
        center.pause_command(self.play, None)
        center.stop_command(self.stop, None)
        center.next_command(self.next, None)
        center.previous_command(self.previous, None)

    def set_playing_progress(self, played_secs, remained_secs):
        total_seconds = int(played_secs + remained_secs)
        percent = (int(played_secs) / total_seconds) * 100
        self.playing_progress.value = percent % 101
        #
        self.lb_playing_left.text = self._format_secs(int(played_secs))
        self.lb_playing_remain.text = self._format_secs(int(remained_secs))

    def previous(self, widget):
        self.parent_layout.previous()  # type: ignore

    def play(self, widget):
        if self.audio_state == AudioState.PLAYING:
            self.parent_layout.pause()  # type: ignore
        else:  # STOP or PAUSED
            self.parent_layout.play()  # type: ignore

    def stop(self, widget):
        self.parent_layout.stop()  # type: ignore

    def next(self, widget):
        self.parent_layout.next()  # type: ignore

    def on_update(self, state: AudioState, audio: Audio, **kwargs):
        match state:
            case AudioState.STOP:
                self.btn_play.icon = Icons.load().play
            case AudioState.PLAYING:
                self.btn_play.icon = Icons.load().pause
            case AudioState.PAUSED:
                self.btn_play.icon = Icons.load().play
        #
        max_width = self.ml_app.main_window.size.width
        self.lb_playing_track.text = audio.track_name_trimmed(max_width)
        #
        self.audio_state = state

    def _format_secs(self, seconds):
        units = {"hours": 3600, "minutes": 60, "seconds": 1}
        values = []
        seconds = int(seconds)
        for unit, value in units.items():
            count = seconds // value
            seconds -= count * value
            values.append(count)
        return f"{values[0]:02d}:{values[1]:02d}:{values[2]:02d}"


class CommonFilesListComponent(TogaComponent):
    def __init__(self, layout: TogaStackedLayout, **kwargs) -> None:
        self._detailedlist = toga.DetailedList(accessors=("name", "length", "icon"),
                                               style=Pack(flex=1),
                                               on_select=self.on_select)
        super().__init__(layout, style=Pack(padding=10, flex=1),
                         children=[self._detailedlist])
        self._selected_index = -1
        self._internal_update = False
        self.audio_state = AudioState.STOP

    @property
    def playlists_list(self) -> toga.DetailedList:
        return self._detailedlist

    @property
    def selected_index(self):
        return self._selected_index

    @selected_index.setter
    def selected_index(self, value):
        self._selected_index = value

    @property
    def selected_audio(self) -> Audio:
        if len(self.playlists_list.data) == 0:
            return Audio.create()

        node: Source_ROW | None = None
        if self.selected_index == -1:
            if (len(self.playlists_list.data) == 0):  # type: ignore
                return Audio.create()
            else:
                node = self.playlists_list.data[0]
        else:
            # Get the playlist name from the parent node
            # and find it in the settings
            if self.selected_index >= len(self.playlists_list.data):
                node = self.playlists_list.data[-1]
                self._selected_index = node.index
            else:
                node = self.playlists_list.data[self.selected_index]

        track = self.ml_app.settings.find_track(node.playlist,  # type: ignore
                                                node.name)
        return Audio(track, node.playlist, self.selected_index)

    def on_select(self, widget):
        # To be implemented in subclasses
        pass

    def previous_index(self, index):
        # Find the previous node in the list
        if index == 0:
            return len(self.playlists_list.data) - 1
        return index - 1

    def next_index(self, index):
        # Find the next node in the list
        if index == len(self.playlists_list.data) - 1:
            return 0
        return index + 1

    def _icon(self, state: AudioState):
        match state:
            case AudioState.PLAYING:
                return Icons.load().sound
            case AudioState.PAUSED:
                return Icons.load().no_sound
            case _:  # Stop, Adding, Removing
                return Icons.load().note


class CommonPlayerLayout(TogaStackedLayout):
    def __init__(self, app: TogaMultiLayoutApp, *types):
        super().__init__(app,
                         *types)

        self.player_thread = None
        self.player_thread_factory = None
        self.audio = Audio.create()

    @property
    def player_deck(self) -> PlayerDeckComponent:
        return self[PlayerDeckComponent]

    def on_load(self):
        if self.audio.playlist_name == "":
            # Get the first playlist name
            self.audio.playlist_name = self.ml_app.settings.get_last_playlist()
        # Load the playlist
        self.on_update(state=AudioState.LOADING,
                       audio=self.audio)
        return super().on_load()

    def add_files(self, paths: list[Path], delete_original: bool = False):

        for path in sorted(paths, key=lambda p: p.name):
            new_mp3 = mp3.load(path)
            # Check if the track is already in the playlist
            # and copy the mp3 file to the playlist directory
            # only if it is not already there
            if len(self.ml_app.settings.search_tracks(self.audio.playlist_name,
                                                      new_mp3.name)) == 0:
                # Copy the mp3 file to the playlist directory
                new_mp3.copy_to(self.ml_app.data_path /
                                new_mp3.relative_path(
                                    self.audio.playlist_name),
                                delete_original)
                # Add the track to the playlist settings
                self.ml_app.settings.add_track(self.audio.playlist_name,
                                               new_mp3.name,
                                               new_mp3.length,
                                               str(new_mp3.data_path))
                self.ml_app.settings.save()

        if len(paths) != 0:
            self.on_update(state=AudioState.ADDING,
                           audio=self.audio)
            self.audio.track = Audio.empty_track()

    def audio_selected(self):
        self.files_toolbar.on_update(state=AudioState.SELECTING,  # type: ignore
                                     audio=self.audio)

    def remove_file(self):

        if self.files_list.selected_index == -1:  # type: ignore
            return

        PlayingThreadGlobals.status = PlayerStatus.STOP
        # Get the selected track
        audio = self.files_list.selected_audio  # type: ignore
        # Delete the mp3 file first
        mp3_file = mp3.load(Path(audio.track.path))
        mp3_file.delete()
        # Remove the track from the playlist settings
        self.ml_app.settings.remove_track(audio.playlist_name, audio.track)
        # Save the settings
        self.ml_app.settings.save()
        #
        self.on_update(state=AudioState.REMOVING,
                       audio=self.audio)
        #
        self.audio.track = Audio.empty_track()

    def previous(self):
        if self.audio.is_empty_track():
            audio = self.files_list.selected_audio  # type: ignore
            if audio.index == -1:  # empty playlist
                return
            self.audio = audio

        # Find the next track in the playlist
        self.audio.track = self.ml_app.settings.find_previous_track(
            self.audio.playlist_name,
            self.audio.track)
        # Play the previous track
        self.audio.index = self.files_list.previous_index(  # type: ignore
            self.audio.index)
        self.files_list.selected_index = self.audio.index  # type: ignore
        self.play_selected_track(self.audio)

    def next(self):
        if self.audio.is_empty_track():
            audio = self.files_list.selected_audio  # type: ignore
            if audio.index == -1:  # empty playlist
                return
            self.audio = audio
        # Find the next track in the playlist
        self.audio.track = self.ml_app.settings.find_next_track(
            self.audio.playlist_name,
            self.audio.track)
        # Play the next track
        self.audio.index = self.files_list.next_index(  # type: ignore
            self.audio.index)
        self.files_list.selected_index = self.audio.index  # type: ignore
        self.play_selected_track(self.audio)

    def play(self):
        # first time playing or  user selected another track
        if (self.audio.is_empty_track() or
                self.audio.index != self.files_list.selected_index):  # type: ignore
            # Get the selected track
            audio = self.files_list.selected_audio  # type: ignore
            if audio.index == -1:  # empty playlist
                return
            self.audio = audio
            # Play the track
            self.play_selected_track(self.audio)
            return
        # Start playing the paused track
        PlayingThreadGlobals.status = PlayerStatus.PLAY
        #
        self.on_update(state=AudioState.PLAYING,
                       audio=self.audio)

    def pause(self):
        if self.audio.is_empty_track():  # empty playlist
            return

        PlayingThreadGlobals.status = PlayerStatus.PAUSE
        #
        self.on_update(state=AudioState.PAUSED,
                       audio=self.audio)

    def stop(self):
        PlayingThreadGlobals.status = PlayerStatus.STOP
        if self.audio.is_empty_track():  # empty playlist
            return
        #
        self.audio.track = Audio.empty_track()
        #
        self.on_update(state=AudioState.STOP,
                       audio=self.audio)

    def play_selected_track(self, player_data):
        PlayingThreadGlobals.status = PlayerStatus.STOP
        if self.player_thread is not None:
            try:
                self.progress_thread.join()
                self.player_thread.join()
            except RuntimeError:
                # If the thread is already stopped, ignore the error
                # It happens when the play_loop is called by the
                # thread itself
                pass
            self.player_thread = None
            # If the track is already playing, stop it
        self.on_update(state=AudioState.PLAYING,
                       audio=self.audio)
        # Play the track
        mp3_file = mp3.load(Path(self.audio.track.path))
        # The play loop must be called by the main loop
        # Otherwise, MacOS will terminate the app
        # (NSInternalInconsistencyException), since the
        # UI element is not updated by the other thread

        def player_loop_main_thread_callback():
            self.promise(lambda: self.play_loop())

        self.player_thread = self.player_thread_factory(
            mp3_file,
            end_callback=player_loop_main_thread_callback)  # type: ignore

        # The progress bar must be updated by the main loop
        # Read the comment above
        def player_progress_main_thread_callback(played_secs, remained_secs):
            self.promise(lambda: self.player_deck.set_playing_progress(played_secs,
                                                                       remained_secs))

        self.progress_thread = ProgressThread(
            player_progress_main_thread_callback)
        PlayingThreadGlobals.status = PlayerStatus.PLAY
        self.player_thread.start()
        self.progress_thread.start()

    def play_loop(self):
        PlayingThreadGlobals.status = PlayerStatus.STOP
        self.next()

    def show_playlists(self):
        # Stop the player thread first
        self.stop()
        if self.player_thread is not None:
            try:
                self.progress_thread.join()
                self.player_thread.join()
            except RuntimeError:
                pass
        self.audio = Audio.create()
        self.files_list.selected_index = -1  # type: ignore
        self.ml_app.show_playlists()  # type: ignore

    def on_end(self):
        PlayingThreadGlobals.status = PlayerStatus.STOP
        if self.audio is not None:
            self.ml_app.settings.set_last_playlist(self.audio.playlist_name)
        return super().on_end()
