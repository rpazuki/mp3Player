from __future__ import annotations

import logging

import toga
from pyMOSF.core import Event, EventType, ServiceRegistry
from pyMOSF.toga import TogaComponent, TogaMultiLayoutApp, TogaStackedLayout
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


class IOSFilesToolbarComponent(TogaComponent):
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
                # toga.Button(icon=icons.delete,
                #             on_press=self.remove_file,
                #             style=icon_style),
        ])
        self.add_btn = self.children[1]
        # self.remove_btn = self.children[2]

    @property
    def parent_layout(self) -> IOSPlayerLayout:
        return self._layout  # type: ignore

    def on_ios_config(self):
        from pyMOSF.services.open_file_ios import IOSFileOpen
        registry = ServiceRegistry()
        registry.bind_event(Event("add_file",
                                  EventType.ON_PRESS,
                                  IOSFileOpen(initial_directory=self.ml_app.data_path,
                                              file_types=["UTTypeMP3"]),
                                  service_callback=self.add_files_ios))

    def on_ipados_config(self):
        from pyMOSF.services.open_file_ios import IOSFileOpen
        registry = ServiceRegistry()
        registry.bind_event(Event("add_file",
                                  EventType.ON_PRESS,
                                  IOSFileOpen(initial_directory=self.ml_app.data_path,
                                              file_types=["UTTypeMP3"]),
                                  service_callback=self.add_files_ios))

    def view_playlsits(self, widget):
        self.parent_layout.show_playlists()  # type: ignore

    def add_files_ios(self, selected):
        self.parent_layout.add_files(
            selected.files, delete_original=True)  # type: ignore

    def on_update(self, state: AudioState, audio: Audio, **kwargs):
        match state:
            case AudioState.PLAYING:
                self.add_btn.enabled = False
            case AudioState.PAUSED:
                self.add_btn.enabled = False
            case AudioState.SELECTING:
                self.add_btn.enabled = True
            case _:  # LOADING, STOP, ADDING, REMOVING
                self.add_btn.enabled = True


class IOSFilesListComponent(CommonFilesListComponent):
    def __init__(self, layout: TogaStackedLayout, **kwargs) -> None:
        super().__init__(layout, **kwargs)
        self._detailedlist.on_primary_action = self.delete_action
        self._detailedlist.primary_action = "Delete"  # type: ignore

    def on_select(self, widget):
        if self._internal_update:
            return
        self._internal_update = True
        node: Source_ROW | None = self.playlists_list.selection
        if node is not None:
            self._selected_index = self.playlists_list.data.index(node)
            self.parent_layout.play()  # type: ignore
        self._internal_update = False

    def delete_action(self, widget, row, **kwargs):
        if (self.audio_state != AudioState.PLAYING and
                self.audio_state != AudioState.PAUSED):
            self._selected_index = row.index
            self.parent_layout.remove_file()  # type: ignore

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


class IOSPlayerLayout(CommonPlayerLayout):
    def __init__(self, app: TogaMultiLayoutApp):
        super().__init__(app,
                         IOSFilesToolbarComponent,
                         IOSFilesListComponent,
                         PlayerDeckComponent)

    @property
    def files_toolbar(self) -> IOSFilesToolbarComponent:
        return self[IOSFilesToolbarComponent]

    @property
    def files_list(self) -> IOSFilesListComponent:
        return self[IOSFilesListComponent]

    def ios_player_factory(self, mp3_file, end_callback):
        from mp3Player.services.players_ios import IOSPlayerThread
        return IOSPlayerThread(
            mp3_file,
            end_callback)

    def on_ios_config(self):
        self.player_thread_factory = self.ios_player_factory

    def on_ipados_config(self):
        self.player_thread_factory = self.ios_player_factory
