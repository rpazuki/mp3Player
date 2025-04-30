
import logging

import toga
from pyMOSF.toga import TogaComponent, TogaMultiLayoutApp, TogaStackedLayout
from toga.sources import Row as Source_ROW
from toga.style import Pack
from toga.style.pack import CENTER, COLUMN, ROW  # type: ignore

from mp3Player.icons import Icons
from mp3Player.toga.playlist_layouts import (
    CommonPlaylistLayout,
    CommonPlaylistToolbarComponent,
    PlaylistState,
)

log = logging.getLogger(__name__)


class IOSPlaylistToolbarComponent(CommonPlaylistToolbarComponent):
    def __init__(self, layout: TogaStackedLayout, **kwargs) -> None:
        icons = Icons.load()
        icon_style = Pack(width=48,
                          height=46,
                          padding=2)
        buttons_box = toga.Box(style=Pack(direction=ROW, alignment=CENTER),
                               children=[
            toga.Button(icon=icons.address_book_add,
                        on_press=self.add_playlist,
                        style=icon_style),
        ])
        self.edit_box = toga.Box(style=Pack(direction=ROW, alignment=CENTER),
                                 children=[
            toga.TextInput("", style=Pack(width=200)),
            toga.Button(icon=icons.success,
                        on_press=self.accept_playlist,
                        style=icon_style),
            toga.Button(icon=icons.cancel,
                        on_press=self.reject_playlist,
                        style=icon_style),
        ]
        )
        self.btn_add_playlist = buttons_box.children[0]  # type: ignore

        self.playlist_textbox = self.edit_box.children[0]  # type: ignore
        self.btn_ok = self.edit_box.children[1]  # type: ignore
        self.btn_cancel = self.edit_box.children[2]  # type: ignore

        self.toolbar_box = toga.Box(style=Pack(direction=COLUMN, alignment=CENTER),
                                    children=[buttons_box,])
        super().__init__(layout,
                         self.playlist_textbox,
                         style=Pack(
                             direction=ROW, alignment=CENTER, padding=1),
                         children=[self.toolbar_box])

    def on_update(self, state: PlaylistState, playlist_name: str, **kwargs):
        self.state = state
        match state:
            case PlaylistState.LOADING | PlaylistState.VIEWING:
                self.toolbar_box.remove(self.edit_box)
                self.btn_add_playlist.enabled = True
                self.playlist_textbox.value = ""
            case PlaylistState.ADDING | PlaylistState.REMOVING:
                self.toolbar_box.add(self.edit_box)
                self.btn_add_playlist.enabled = False
                self.playlist_textbox.focus()
            case PlaylistState.EDITING:
                self.toolbar_box.add(self.edit_box)
                self.btn_add_playlist.enabled = False
                self.playlist_textbox.value = playlist_name.strip()
                self.playlist_textbox.focus()
            case PlaylistState.SELECTING:
                self.btn_add_playlist.enabled = True


class IOSPlaylistsListComponent(TogaComponent):
    def __init__(self, layout: TogaStackedLayout, **kwargs) -> None:
        self.__playlists = toga.DetailedList(accessors=("name", "file_number", "picture"),
                                             style=Pack(flex=1),
                                             on_select=self.on_select,
                                             on_primary_action=self.remove_action,
                                             primary_action="Delete",
                                             on_secondary_action=self.edit_action,
                                             secondary_action="Edit",
                                             )
        super().__init__(layout, style=Pack(padding=10, flex=1),
                         children=[self.__playlists])
        self._selected_index = -1
        self._internal_update = False
        self.playlist_state = PlaylistState.LOADING
        self.c = 0

    @property
    def playlists_list(self) -> toga.DetailedList:
        return self.__playlists

    @property
    def selected_index(self):
        return self._selected_index

    @property
    def selected_playlist(self) -> str:
        if len(self.playlists_list.data) == 0:
            return ""
        #
        node: Source_ROW | None = None
        if self.selected_index == -1:
            if (len(self.playlists_list.data) == 0):  # type: ignore
                return ""
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
        #
        playlist = self.ml_app.settings.find_playlist(node.name)
        return playlist.name

    def on_select(self, widget):
        if self._internal_update:
            return
        node: Source_ROW | None = self.playlists_list.selection
        if node is not None:
            self._selected_index = self.playlists_list.data.index(
                node)
            self.parent_layout.view_play_deck()  # type: ignore
        self._internal_update = False

    def remove_action(self, widget, row, **kwargs):
        self._selected_index = row.index
        self.parent_layout.remove_playlist()  # type: ignore

    def edit_action(self, widget, row, **kwargs):
        self._selected_index = row.index
        self.parent_layout.show_edit_playlist()  # type: ignore

    def on_update(self, state: PlaylistState, playlist_name: str, **kwargs):
        self.playlist_state = state

        # if state == PlaylistState.LOADING:
        #     self._selected_index = -1
        #
        self._internal_update = True
        self.playlists_list.data.clear()
        for i, playlist in enumerate(self.ml_app.settings.Playlists):
            self.playlists_list.data.append({
                "picture": Icons.load().address_book,
                "name": playlist.name,  # type: ignore
                "file_number": len(playlist.tracks),  # type: ignore
                "index": i
            })
        self._internal_update = False


class IOSPlaylistLayout(CommonPlaylistLayout):
    def __init__(self, app: TogaMultiLayoutApp):
        super().__init__(app,
                         IOSPlaylistToolbarComponent,
                         IOSPlaylistsListComponent)

    @property
    def toolbar(self) -> IOSPlaylistToolbarComponent:
        return self[IOSPlaylistToolbarComponent]

    @property
    def playlists_tree(self) -> IOSPlaylistsListComponent:
        return self[IOSPlaylistsListComponent]
