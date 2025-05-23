from __future__ import annotations

import logging

import toga
from pyMOSF.core import Event, EventType, ServiceRegistry
from pyMOSF.toga import TogaComponent, TogaMultiLayoutApp, TogaStackedLayout
from pyMOSF.toga.services import FileOpen
from toga.sources import Row as Source_ROW
from toga.style import Pack
from toga.style.pack import CENTER, ROW  # type: ignore

from mp3Player.icons import Icons
from mp3Player.toga.player_layouts import (
    Audio,
    AudioState,
    CommonFilesListComponent,
    CommonPlayerLayout,
    PlayerDeckComponent,
)

log = logging.getLogger(__name__)


class MacOSFilesToolbarComponent(TogaComponent):
    def __init__(self, layout: TogaStackedLayout, **kwargs) -> None:
        icons = Icons.load()
        icon_style = Pack(width=48,
                          height=46,
                          padding=2)
        super().__init__(layout, style=Pack(
            direction=ROW, alignment=CENTER, padding=1),
            children=[
                toga.Button(icon=icons.address_book,
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
        self.remove_btn = self.children[2]
       

    @property
    def parent_layout(self) -> MacOSPlayerLayout:
        return self._layout  # type: ignore


    def on_darwin_config(self):
        ServiceRegistry().bind_event(Event("add_file",
                                           EventType.ON_PRESS,
                                           FileOpen(file_types=["mp3"],
                                                    multiple_select=True),
                                           service_callback=self.add_files))

    def view_playlsits(self, widget):
        self.parent_layout.show_playlists()  # type: ignore

    def add_files(self, selected):
        self.parent_layout.add_files(
            selected.files, delete_original=False)  # type: ignore

    def remove_file(self, widget):
        self.parent_layout.remove_file()  # type: ignore

    def on_update(self, state: AudioState, audio: Audio, **kwargs):
        match state:
            case AudioState.PLAYING:
                self.add_btn.enabled = False
                self.remove_btn.enabled = False
            case AudioState.PAUSED:
                self.add_btn.enabled = False
                self.remove_btn.enabled = False
            case AudioState.SELECTING:
                self.remove_btn.enabled = True
                self.add_btn.enabled = True
            case _:  # LOADING, STOP, ADDING, REMOVING
                self.add_btn.enabled = True
                self.remove_btn.enabled = False


class MacOSFilesListComponent(CommonFilesListComponent):

    def on_select(self, widget):
        if self._internal_update:
            return
        self._internal_update = True
        node: Source_ROW | None = self.playlists_list.selection
        self._selected_index = self.playlists_list.data.index(
            node) if node is not None else -1

        if self._selected_index == -1:
            self._internal_update = False
            return

        if (self.audio_state != AudioState.PLAYING and
              self.audio_state != AudioState.PAUSED):
            self.parent_layout.audio_selected()  # type: ignore
        else:
            self.parent_layout.play()  # type: ignore
        self._internal_update = False

    def on_update(self, state: AudioState, audio: Audio, **kwargs):
        self.audio_state = state
        if audio.playlist_name == "":
            return

        def later():
            self._internal_update = True
            playlist = self.ml_app.settings.find_playlist(audio.playlist_name)
            self._internal_update = True
            self.playlists_list.data.clear()
            for i, track in enumerate(playlist.tracks):
                self.playlists_list.data.append({
                    "icon": Icons.load().note if i != audio.index else self._icon(state),
                    "name": track.name,
                    "length": track.length,
                    "playlist": playlist.name,
                    "index": i})
            if audio.index < len(playlist.tracks):
                self.playlists_list.scroll_to_row(audio.index)
            self._internal_update = False

        self.promise(later)


class MacOSPlayerLayout(CommonPlayerLayout):
    def __init__(self, app: TogaMultiLayoutApp):
        super().__init__(app,
                         MacOSFilesToolbarComponent,
                         MacOSFilesListComponent,
                         PlayerDeckComponent)

    @property
    def files_toolbar(self) -> MacOSFilesToolbarComponent:
        return self[MacOSFilesToolbarComponent]

    @property
    def files_list(self) -> MacOSFilesListComponent:
        return self[MacOSFilesListComponent]

    def player_factory(self, mp3_file, end_callback):
        from mp3Player.services import PlayerThread
        return PlayerThread(
            mp3_file,
            end_callback)

    def on_darwin_config(self):
        self.player_thread_factory = self.player_factory
