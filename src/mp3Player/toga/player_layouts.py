from __future__ import annotations

import logging
from pathlib import Path

import toga

# , silence_crossed_events
from toga.sources import Node
from toga.sources import Row as Source_ROW
from toga.style import Pack
from toga.style.pack import CENTER, COLUMN, ROW  # type: ignore

from mp3Player.config import Dict
from mp3Player.core import Event, EventType, ServiceRegistry
from mp3Player.services import PlayerStatus, PlayingThreadGlobals, ProgressThread, mp3
from mp3Player.toga import TogaComponent, TogaMultiLayoutApp, TogaStackedLayout
from mp3Player.toga.icons import Icons
from mp3Player.toga.services.io import FileOpenOpenCV

log = logging.getLogger(__name__)


class FilesToolbarComponent(TogaComponent):
    def __init__(self, layout: TogaStackedLayout, **kwargs) -> None:
        icons = Icons.load()
        icon_style = Pack(width=48,
                          height=46,
                          padding=2)
        super().__init__(layout, style=Pack(
            direction=ROW, alignment=CENTER, padding=1),
            children=[
                toga.Button(icon=icons.report,
                            on_press=self.view_playlsits,
                            style=icon_style),
                toga.Button(icon=icons.add,
                            id="add_file",
                            style=icon_style),
                toga.Button(icon=icons.delete,
                            on_press=self.remove_file,
                            style=icon_style),
        ])
        self.add_btn = self.children[1]
        # self.add_btn.on_press = self.pre_add_file

    def on_ios_config(self):
        # def on_dispatch(widget):
        #     self.parent_layout.add_files([])  # type: ignore
        # self.add_btn.on_press = on_dispatch
        ##
        from mp3Player.services.open_file_ios import IOSFileOpen
        registry = ServiceRegistry()
        registry.bind_event(
            Event("add_file",
                  EventType.ON_PRESS,
                  IOSFileOpen(self.ml_app.data_path),
                  service_callback=self.add_files_ios)
        )

    def on_ipados_config(self):
        # def on_dispatch(widget):
        #     self.parent_layout.add_files([])  # type: ignore
        # self.add_btn.on_press = on_dispatch
        ##
        from mp3Player.services.open_file_ios import IOSFileOpen
        registry = ServiceRegistry()
        registry.bind_event(
            Event("add_file",
                  EventType.ON_PRESS,
                  IOSFileOpen(self.ml_app.data_path),
                  service_callback=self.add_files_ios)
        )

    @property
    def parent_layout(self) -> PlayerLayout:
        return self._layout  # type: ignore

    def on_linux_config(self):
        ##
        registry = ServiceRegistry()
        registry.bind_event(
            Event("add_file",
                  EventType.ON_PRESS,
                  FileOpenOpenCV(),
                  service_callback=self.add_files)
        )

    def on_windows_config(self):
        ##
        registry = ServiceRegistry()
        registry.bind_event(
            Event("add_file",
                  EventType.ON_PRESS,
                  FileOpenOpenCV(),
                  service_callback=self.add_files)
        )

    def on_darwin_config(self):
        ##
        registry = ServiceRegistry()
        registry.bind_event(
            Event("add_file",
                  EventType.ON_PRESS,
                  FileOpenOpenCV(),
                  service_callback=self.add_files)
        )

    def view_playlsits(self, widget):
        self.parent_layout.ml_app.show_playlists()  # type: ignore

    def add_files(self, paths):
        self.parent_layout.add_files(
            paths, delete_original=False)  # type: ignore

    def add_files_ios(self, paths):
        self.parent_layout.add_files(
            paths, delete_original=True)  # type: ignore

    def remove_file(self, widget):
        self.parent_layout.remove_file()  # type: ignore


class PlayerDeckComponent(TogaComponent):
    def __init__(self, layout: TogaStackedLayout, **kwargs) -> None:
        icons = Icons.load()
        icon_style = Pack(width=50,
                          height=48,
                          padding_bottom=4)  # , background_color="#666666")
        buttons_box = toga.Box(style=Pack(direction=ROW, alignment=CENTER),
                               children=[
                                   toga.Button(icon=icons.rewind,
                                               on_press=self.previous,
                                               style=icon_style),
            toga.Button(icon=icons.play,
                                       on_press=self.play,
                                       style=icon_style),
            toga.Button(icon=icons.stop,
                                       on_press=self.stop,
                                       style=icon_style),
            toga.Button(icon=icons.forward,
                                       on_press=self.next,
                                       style=icon_style),
        ])
        playing_track_box = toga.Box(style=Pack(direction=ROW, alignment=CENTER),
                                     children=[
            # toga.Button(icon=icons.nosound,
            #             on_press=self.play),
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
        self.is_playing = False
        self.btn_play = buttons_box.children[1]
        self.btn_stop = buttons_box.children[2]
        # self.im_playing_track = playing_track_box.children[0]
        self.lb_playing_track = playing_track_box.children[0]
        self.lb_playing_left = playing_progress_box.children[0]
        self.playing_progress = playing_progress_box.children[1]
        self.lb_playing_remain = playing_progress_box.children[2]

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

    def update_player_deck_status(self,
                                  track_name: str,
                                  player_status: PlayerStatus):
        max_width = self.ml_app.main_window.size.width
        char_size = 10
        char_nums = int(max_width / char_size) - 3

        if char_nums <= len(track_name):
            self.lb_playing_track.text = track_name[:char_nums] + "..."
        else:
            self.lb_playing_track.text = track_name
        # self.im_playing_track.icon = self._sound_icon(player_status)
        self.btn_play.icon = self._play_btn_icon(player_status)
        if player_status == PlayerStatus.PLAY:
            self.is_playing = True
        else:
            self.is_playing = False

    def set_playing_progress(self, played_secs, remained_secs):
        total_seconds = int(played_secs + remained_secs)
        percent = (int(played_secs) / total_seconds) * 100
        self.playing_progress.value = percent % 101
        #
        self.lb_playing_left.text = self._format_secs(int(played_secs))
        self.lb_playing_remain.text = self._format_secs(int(remained_secs))

    def previous(self, widget):
        self.is_playing = True
        self.parent_layout.previous()  # type: ignore

    def play(self, widget):
        if self.is_playing:
            self.is_playing = False
            self.parent_layout.pause()  # type: ignore
        else:
            self.is_playing = True
            self.parent_layout.play()  # type: ignore

    def stop(self, widget):
        self.is_playing = False
        self.parent_layout.stop()  # type: ignore

    def next(self, widget):
        self.is_playing = True
        self.parent_layout.next()  # type: ignore

    def _format_secs(self, seconds):
        units = {"hours": 3600, "minutes": 60, "seconds": 1}
        values = []
        seconds = int(seconds)
        for unit, value in units.items():
            count = seconds // value
            seconds -= count * value
            values.append(count)
        return f"{values[0]:02d}:{values[1]:02d}:{values[2]:02d}"

    def _sound_icon(self, status: PlayerStatus):
        match status:
            case PlayerStatus.PLAY:
                return Icons.load().sound
            case PlayerStatus.PAUSE:
                return Icons.load().nosound
            case PlayerStatus.STOP:
                return Icons.load().nosound

    def _play_btn_icon(self, status: PlayerStatus):
        match status:
            case PlayerStatus.PLAY:
                return Icons.load().pause
            case PlayerStatus.PAUSE:
                return Icons.load().play
            case PlayerStatus.STOP:
                return Icons.load().play


class FilesListComponent(TogaComponent):
    def __init__(self, layout: TogaStackedLayout, **kwargs) -> None:
        self.__playlists = toga.DetailedList(accessors=("name", "length", "picture"),
                                             style=Pack(flex=1),
                                             on_select=self.on_select,
                                             )
        super().__init__(layout, style=Pack(padding=10, flex=1),
                         children=[self.__playlists])
        self.last_selected_node = None
        self.last_selected_node_changed = False
        self._internal_update = False

    @property
    def playlists_list(self) -> toga.DetailedList:
        return self.__playlists

    def on_common_config(self):
        ############
        # Settings
        self.settings = self.ml_app.settings
        #

    def on_select(self, widget):
        if self._internal_update:
            return
        node: Source_ROW | None = self.playlists_list.selection
        if node != self.last_selected_node:
            self.last_selected_node_changed = True
        else:
            self.last_selected_node_changed = False
        self.last_selected_node: Source_ROW | None = node
        self.parent_layout.select_track()  # type: ignore

    def load_playlist(self,
                      playlist_name="",
                      playing_index: int = -1,
                      player_status: PlayerStatus = PlayerStatus.STOP):
        if playlist_name == "":
            return

        playlist = self.settings.find_playlist(playlist_name)
        self._internal_update = True
        self.playlists_list.data.clear()
        for i, track in enumerate(playlist.tracks):
            self.playlists_list.data.append({
                "picture": Icons.load().mp3 if i != playing_index else self._icon(player_status),
                "name": track.name,
                "length": track.length,
                "playlist": playlist.name,
                "index": i})
        self._internal_update = False

    def is_track_selected(self):
        node: Node = self.playlists_list.selection  # type: ignore
        if node is None:  # No selection or playlist selection
            return False
        return True

    def reset_selected_node(self):
        self.last_selected_node = None
        self.last_selected_node_changed = False
        self.last_selected_node_changed = False
        self._internal_update = False

    def selected_track(self) -> tuple[Source_ROW, str, Dict] | tuple[None, str, Dict]:
        # If no track is selected, select one
        if self.last_selected_node is None:
            if (len(self.playlists_list.data) == 0):  # type: ignore
                return (None, "", Dict({}))
            # type: ignore
            self.last_selected_node = self.playlists_list.data[0]

        # Get the playlist name from the parent node
        # and find it in the settings
        playlist_name = self.last_selected_node.playlist  # type: ignore
        self.last_selected_node_changed = False
        return (self.last_selected_node,
                playlist_name,
                self.settings.find_track(playlist_name, self.last_selected_node.name))

    def add_track_to_playlist_tree(self, playlist_name, mp3_name, mp3_length):
        self.playlists_list.data.append({
            "picture": Icons.load().mp3,
            "name": mp3_name,
            "length": mp3_length,
            "playlist": playlist_name,
            "index": len(self.playlists_list.data)
        })

    def remove_track_from_playlist_tree(self, tree_node):
        self.playlists_list.data.remove(tree_node)

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

    def _icon(self, status: PlayerStatus):
        match status:
            case PlayerStatus.PLAY:
                return Icons.load().sound
            case PlayerStatus.PAUSE:
                return Icons.load().nosound
            case PlayerStatus.STOP:
                return Icons.load().mp3


class PlayerLayout(TogaStackedLayout):
    def __init__(self, app: TogaMultiLayoutApp):
        super().__init__(app,
                         FilesToolbarComponent,
                         FilesListComponent,
                         PlayerDeckComponent)

        self.player_thread = None
        self.player_thread_factory = None
        self.last_played_track = None
        self.last_played_track_index = -1
        self.playlist_name = ""

    @property
    def files_list(self) -> FilesListComponent:
        return self[FilesListComponent]

    @property
    def player_deck(self) -> PlayerDeckComponent:
        return self[PlayerDeckComponent]

    def on_common_config(self):
        ############
        # Settings
        self.settings = self.ml_app.settings

    def player_factory(self, mp3_file, end_callback):
        from mp3Player.services import PlayerThread
        return PlayerThread(
            mp3_file,
            end_callback)

    def ios_player_factory(self, mp3_file, end_callback):
        from mp3Player.services.players_ios import IOSPlayerThread
        return IOSPlayerThread(
            mp3_file,
            end_callback)

    def on_ios_config(self):
        self.player_thread_factory = self.ios_player_factory

    def on_ipados_config(self):
        self.player_thread_factory = self.ios_player_factory

    def on_linux_config(self):
        self.player_thread_factory = self.player_factory

    def on_windows_config(self):
        self.player_thread_factory = self.player_factory

    def on_darwin_config(self):
        self.player_thread_factory = self.player_factory

    def on_load(self):
        if self.playlist_name == "":
            # Get the first playlist name
            # self.playlist_name = self.settings.Playlists[0].name
            self.playlist_name = self.settings.get_last_playlist()

        self.files_list.load_playlist(self.playlist_name)
        return super().on_load()

    def add_files(self, paths, delete_original: bool = False):
        # if len(paths) == 0:
        #     paths = [Icons.load().mp3_sample,
        #              Icons.load().mp3_sample_2,]

        if len(paths) != 0:
            PlayingThreadGlobals.status = PlayerStatus.STOP

        for path in sorted(paths, key=lambda p: p.name):
            new_mp3 = mp3.load(path)  # type: ignore
            # Check if the track is already in the playlist
            # and copy the mp3 file to the playlist directory
            # only if it is not already there
            if len(self.settings.search_tracks(self.playlist_name, new_mp3.name)) == 0:
                # Copy the mp3 file to the playlist directory
                new_mp3.copy_to(self.ml_app.data_path /
                                new_mp3.relative_path(self.playlist_name),
                                delete_original)
                # Add the track to the playlist settings
                self.settings.add_track(self.playlist_name,
                                        new_mp3.name,
                                        new_mp3.length,
                                        str(new_mp3.data_path))
                # Add the track to the tree
                self.files_list.add_track_to_playlist_tree(
                    self.playlist_name,
                    new_mp3.name,
                    new_mp3.length)
                self.settings.save()

        if len(paths) != 0:
            self.files_list.load_playlist(
                self.playlist_name, -1, PlayerStatus.STOP)
            self.files_list.reset_selected_node()
            self.player_deck.update_player_deck_status("", PlayerStatus.STOP)
            self.last_played_track = None

    def remove_file(self):

        if not self.files_list.is_track_selected():
            return

        PlayingThreadGlobals.status = PlayerStatus.STOP
        # Get the selected track
        _, playlist_name, track = self.files_list.selected_track()
        # Delete the mp3 file first
        mp3_file = mp3.load(Path(track.path))
        mp3_file.delete()
        # Remove the track from the playlist settings
        self.settings.remove_track(playlist_name, track)
        # Remove the track from the tree
        # self.files_list.remove_track_from_playlist_tree(tree_node)
        # Save the settings
        self.settings.save()
        #
        self.files_list.load_playlist(playlist_name, -1, PlayerStatus.STOP)
        self.files_list.reset_selected_node()
        self.player_deck.update_player_deck_status("", PlayerStatus.STOP)
        #
        self.last_played_track = None

    def previous(self):
        if self.last_played_track is not None:
            track = self.last_played_track
            playlist_name = self.playlist_name
            index = self.last_played_track_index
        else:
            row, playlist_name, track = self.files_list.selected_track()
            if row is None:  # empty playlist
                return
            index = row.index

        # Find the next track in the playlist
        track = self.settings.find_previous_track(playlist_name,  # type: ignore
                                                  track)
        # Play the previous track
        previous_index = self.files_list.previous_index(index)
        self.play_selected_track(track,
                                 playlist_name,
                                 previous_index)  # type: ignore

    def next(self):
        if self.last_played_track is not None:
            track = self.last_played_track
            playlist_name = self.playlist_name
            index = self.last_played_track_index
        else:
            row, playlist_name, track = self.files_list.selected_track()
            if row is None:  # empty playlist
                return
            index = row.index

        # Find the next track in the playlist
        track = self.settings.find_next_track(playlist_name,  # type: ignore
                                              track)
        # Play the next track
        next_index = self.files_list.next_index(index)
        self.play_selected_track(track,
                                 playlist_name,
                                 next_index)  # type: ignore

    def select_track(self):
        # Since we cannot catch double click, we only let
        # the user to select aother track after it starts playing
        # TODO: must suport it only on linux and macOs and windows
        # if PlayingThreadGlobals.status == PlayerStatus.STOP:
        #     return
        # self.play()
        pass

    def play(self):
        if (self.last_played_track is None or  # first play
                self.files_list.last_selected_node_changed):  # user selected another track
            # Get the selected track
            row, playlist, track = self.files_list.selected_track()
            if row is None:  # empty playlist
                return
            self.last_played_track = track
            self.playlist_name = playlist
            self.last_played_track_index = row.index
            # Play the track
            self.play_selected_track(track,
                                     playlist,
                                     row.index)  # type: ignore
            self.player_deck.update_player_deck_status(track.name,
                                                       PlayerStatus.PLAY)
            return
        # Start playing the paused track
        PlayingThreadGlobals.status = PlayerStatus.PLAY
        self.files_list.load_playlist(
            self.playlist_name, self.last_played_track_index, PlayerStatus.PLAY)
        self.player_deck.update_player_deck_status(self.last_played_track.name,
                                                   PlayerStatus.PLAY)

    def pause(self):
        if self.last_played_track is None:  # empty playlist
            return

        PlayingThreadGlobals.status = PlayerStatus.PAUSE
        self.player_deck.update_player_deck_status(self.last_played_track.name,  # type: ignore
                                                   PlayerStatus.PAUSE)
        self.files_list.load_playlist(self.playlist_name,
                                      self.last_played_track_index,
                                      PlayerStatus.PAUSE)

    def stop(self):
        PlayingThreadGlobals.status = PlayerStatus.STOP
        if self.last_played_track_index == -1:  # empty playlist
            return

        self.last_played_track = None
        self.player_deck.update_player_deck_status("",
                                                   PlayerStatus.STOP)
        self.files_list.load_playlist(self.playlist_name,
                                      -1,
                                      PlayerStatus.STOP)

    def play_selected_track(self, track, playlist, index):
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
        self.last_played_track = track
        self.playlist_name = playlist
        self.last_played_track_index = index
        # Update the status of the selected track
        # self.files_list.update_files_list_status(index,
        #                                          PlayerStatus.PLAY)
        self.files_list.load_playlist(playlist, index, PlayerStatus.PLAY)
        self.player_deck.update_player_deck_status(track.name,
                                                   PlayerStatus.PLAY)
        # Play the track
        mp3_file = mp3.load(Path(track.path))  # type: ignore

        # The play loop must be called by the main loop
        # Otherwise, MacOS will terminate the app
        # (NSInternalInconsistencyException), since the
        # UI element is not updated by the other thread
        def player_loop_main_thread_callback():
            def future_callback():
                self.play_loop()
            self.ml_app.loop.call_soon_threadsafe(future_callback)

        self.player_thread = self.player_thread_factory(
            mp3_file,
            end_callback=player_loop_main_thread_callback)  # type: ignore

        # The progress bar must be updated by the main loop
        # Read the comment above
        def player_progress_main_thread_callback(played_secs, remained_secs):
            def future_callback():
                self.player_deck.set_playing_progress(played_secs,
                                                      remained_secs)
            self.ml_app.loop.call_soon_threadsafe(future_callback)

        self.progress_thread = ProgressThread(
            player_progress_main_thread_callback)
        PlayingThreadGlobals.status = PlayerStatus.PLAY
        self.player_thread.start()
        self.progress_thread.start()

    def play_loop(self):
        PlayingThreadGlobals.status = PlayerStatus.STOP
        # Get the selected track

        self.next()

    def on_end(self):
        PlayingThreadGlobals.status = PlayerStatus.STOP
        self.settings.set_last_playlist(self.playlist_name)
        self.settings.last_track = self.last_played_track
        return super().on_end()
