import asyncio
import logging
import re
from enum import Enum

import toga
from toga.sources import Row as Source_ROW
from toga.style import Pack
from toga.style.pack import CENTER, COLUMN, ROW  # type: ignore

from mp3Player.toga import TogaComponent, TogaMultiLayoutApp, TogaStackedLayout
from mp3Player.toga.icons import Icons

log = logging.getLogger(__name__)


class PlaylistState(int, Enum):
    VIEWING = 0
    ADDING = 1
    REMOVING = 2
    EDITING = 3
    SELECTING = 4
    LOADING = 5


class PlaylistToolbarComponent(TogaComponent):
    def __init__(self, layout: TogaStackedLayout, **kwargs) -> None:
        icons = Icons.load()
        icon_style = Pack(width=48,
                          height=46,
                          padding=2)
        buttons_box = toga.Box(style=Pack(direction=ROW, alignment=CENTER),
                               children=[
            # toga.Label("Playlists   ",
            #            style=Pack(padding=2, color="#bb0000")),
            toga.Button(icon=icons.note,
                        on_press=self.view_play_deck,
                        style=icon_style),
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
        self.btn_add_playlist = buttons_box.children[1]  # type: ignore

        self.playlist_textbox = self.edit_box.children[0]  # type: ignore
        self.btn_ok = self.edit_box.children[1]  # type: ignore
        self.btn_cancel = self.edit_box.children[2]  # type: ignore

        self.toolbar_box = toga.Box(style=Pack(direction=COLUMN, alignment=CENTER),
                                    children=[buttons_box,])
        super().__init__(layout, style=Pack(
            direction=ROW, alignment=CENTER, padding=1),
            children=[self.toolbar_box])

        self.state = PlaylistState.LOADING

    @property
    def editing_playlist(self) -> str:
        return self.playlist_textbox.value.strip()

    def view_play_deck(self, widget):
        self.parent_layout.view_play_deck()  # type: ignore

    def add_playlist(self, widget):
        self.parent_layout.show_add_playlist()  # type: ignore

    def accept_playlist(self, widget):
        match self.state:
            case PlaylistState.ADDING:
                if self.playlist_textbox.value.strip() == "":
                    return
                self.parent_layout.add_playlist()  # type: ignore
            case PlaylistState.EDITING:
                if self.playlist_textbox.value.strip() == "":
                    return
                self.parent_layout.edit_playlist()  # type: ignore

    def reject_playlist(self, widget):
        self.parent_layout.cancel_playlist()  # type: ignore

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


class DesktopPlaylistToolbarComponent(TogaComponent):
    def __init__(self, layout: TogaStackedLayout, **kwargs) -> None:
        icons = Icons.load()
        icon_style = Pack(width=48,
                          height=46,
                          padding=2)
        buttons_box = toga.Box(style=Pack(direction=ROW, alignment=CENTER),
                               children=[
            # toga.Label("Playlists   ",
            #            style=Pack(padding=2, color="#bb0000")),
            toga.Button(icon=icons.note,
                        on_press=self.view_play_deck,
                        style=icon_style),
            toga.Button(icon=icons.playlist_add,
                        on_press=self.add_playlist,
                        style=icon_style),
            toga.Button(icon=icons.playlist_delete,
                        on_press=self.remove_playlist,
                        enabled=False,
                        style=icon_style),
            toga.Button(icon=icons.playlist_edit,
                        on_press=self.edit_playlist,
                        enabled=False,
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
        self.btn_add_playlist = buttons_box.children[1]  # type: ignore
        self.btn_remove_playlist = buttons_box.children[2]  # type: ignore
        self.btn_edit_playlist = buttons_box.children[3]  # type: ignore

        self.playlist_textbox = self.edit_box.children[0]  # type: ignore
        self.btn_ok = self.edit_box.children[1]  # type: ignore
        self.btn_cancel = self.edit_box.children[2]  # type: ignore

        self.toolbar_box = toga.Box(style=Pack(direction=COLUMN, alignment=CENTER),
                                    children=[buttons_box,])
        super().__init__(layout, style=Pack(
            direction=ROW, alignment=CENTER, padding=1),
            children=[self.toolbar_box])

        self.state = PlaylistState.LOADING

    @property
    def editing_playlist(self) -> str:
        return self.playlist_textbox.value.strip()

    def view_play_deck(self, widget):
        self.parent_layout.view_play_deck()  # type: ignore

    def add_playlist(self, widget):
        self.parent_layout.show_add_playlist()  # type: ignore

    def remove_playlist(self, widget):
        self.parent_layout.remove_playlist()  # type: ignore

    def edit_playlist(self, widget):
        self.parent_layout.show_edit_playlist()  # type: ignore

    def accept_playlist(self, widget):
        match self.state:
            case PlaylistState.ADDING:
                if self.playlist_textbox.value.strip() == "":
                    return
                self.parent_layout.add_playlist()  # type: ignore
            case PlaylistState.EDITING:
                if self.playlist_textbox.value.strip() == "":
                    return
                self.parent_layout.edit_playlist()  # type: ignore

    def reject_playlist(self, widget):
        self.parent_layout.cancel_playlist()  # type: ignore

    def on_update(self, state: PlaylistState, playlist_name: str, **kwargs):
        self.state = state
        match state:
            case PlaylistState.LOADING | PlaylistState.VIEWING:
                self.toolbar_box.remove(self.edit_box)
                self.btn_add_playlist.enabled = True
                self.btn_remove_playlist.enabled = False
                self.btn_edit_playlist.enabled = False
                self.playlist_textbox.value = ""
            case PlaylistState.ADDING | PlaylistState.REMOVING:
                self.toolbar_box.add(self.edit_box)
                self.btn_add_playlist.enabled = False
                self.btn_remove_playlist.enabled = False
                self.btn_edit_playlist.enabled = False
            case PlaylistState.EDITING:
                self.toolbar_box.add(self.edit_box)
                self.btn_add_playlist.enabled = False
                self.btn_remove_playlist.enabled = False
                self.btn_edit_playlist.enabled = False
                self.playlist_textbox.value = playlist_name.strip()
            case PlaylistState.SELECTING:
                self.btn_add_playlist.enabled = True
                self.btn_remove_playlist.enabled = True
                self.btn_edit_playlist.enabled = True


class PlaylistsListComponent(TogaComponent):
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
        playlist = self.settings.find_playlist(node.name)
        return playlist.name

    def on_select(self, widget):
        if self._internal_update:
            return
        node: Source_ROW | None = self.playlists_list.selection
        if node is not None:
            # temp_index = self.playlists_list.data.index(
            #     node)

            # if temp_index == self._selected_index:
            #     # primary action will be called here
            #     # self._selected_index = -1
            #     pass
            # else:
            #     self._selected_index = temp_index
            #     self.parent_layout.view_play_deck()  # type: ignore
            self._selected_index = self.playlists_list.data.index(
                node)
            self.parent_layout.view_play_deck()  # type: ignore
        self._internal_update = False

    def remove_action(self, widget, row, **kwargs):
        self.parent_layout.remove_playlist()  # type: ignore

    def edit_action(self, widget, row, **kwargs):
        self.parent_layout.show_edit_playlist()  # type: ignore

    def on_update(self, state: PlaylistState, playlist_name: str, **kwargs):
        self.playlist_state = state

        # if state == PlaylistState.LOADING:
        #     self._selected_index = -1
        #
        self._internal_update = True
        self.playlists_list.data.clear()
        self.settings = self.ml_app.settings
        for playlist in self.settings.Playlists:
            self.playlists_list.data.append({
                "picture": Icons.load().address_book,
                "name": playlist.name,  # type: ignore
                "file_number": len(playlist.tracks),  # type: ignore
            })
        self._internal_update = False


class DesktopPlaylistsListComponent(TogaComponent):
    def __init__(self, layout: TogaStackedLayout, **kwargs) -> None:
        self.__playlists = toga.DetailedList(accessors=("name", "file_number", "picture"),
                                             style=Pack(flex=1),
                                             on_select=self.on_select,
                                             )
        super().__init__(layout, style=Pack(padding=10, flex=1),
                         children=[self.__playlists])
        self._selected_index = -1
        self._internal_update = False
        self.playlist_state = PlaylistState.LOADING

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
        playlist = self.settings.find_playlist(node.name)
        return playlist.name

    def on_select(self, widget):
        if self._internal_update:
            return
        node: Source_ROW | None = self.playlists_list.selection
        self._selected_index = self.playlists_list.data.index(
            node) if node is not None else -1

        if self._selected_index == -1:
            return
        #
        if (self.playlist_state == PlaylistState.VIEWING or
                self.playlist_state == PlaylistState.SELECTING):
            self.parent_layout.playlist_selected()  # type: ignore

    def on_update(self, state: PlaylistState, playlist_name: str, **kwargs):
        self.playlist_state = state
        #
        self._internal_update = True
        self.playlists_list.data.clear()
        self.settings = self.ml_app.settings
        for playlist in self.settings.Playlists:
            self.playlists_list.data.append({
                "picture": Icons.load().address_book,
                "name": playlist.name,  # type: ignore
                "file_number": len(playlist.tracks),  # type: ignore
            })
        self._internal_update = False


class PlaylistLayout(TogaStackedLayout):
    def __init__(self, app: TogaMultiLayoutApp):
        super().__init__(app,
                         PlaylistToolbarComponent,
                         PlaylistsListComponent)

        self.message_dialog = toga.InfoDialog(
            "Alert",
            ""
        )
        self.playlist = ""

    def show_dialog(self,
                    message: str,
                    title: str = "Alert",
                    dialog_type=toga.InfoDialog,
                    dialog_callback=None):
        dialog = dialog_type(title=title,
                             message=message)

        task = asyncio.create_task(
            self.ml_app.main_window.dialog(dialog))  # type: ignore

        def dummy(task): return None
        if dialog_callback is None:
            dialog_callback = dummy
        task.add_done_callback(dialog_callback)

    @property
    def toolbar(self) -> PlaylistToolbarComponent:
        return self[PlaylistToolbarComponent]

    @property
    def playlists_tree(self) -> PlaylistsListComponent:
        return self[PlaylistsListComponent]

    def on_common_config(self):
        ############
        # Settings
        self.settings = self.ml_app.settings

    def on_load(self):
        # Load the list of playlists
        self.on_update(state=PlaylistState.LOADING,
                       playlist_name=self.playlist)
        return super().on_load()

    # Only called in Win version
    def playlist_selected(self):
        self.playlist = self.playlists_tree.selected_playlist
        self.toolbar.on_update(state=PlaylistState.SELECTING,
                               playlist_name=self.playlist)

    def show_add_playlist(self):
        self.playlist = ""
        self.on_update(state=PlaylistState.ADDING,
                       playlist_name=self.playlist)

    def show_edit_playlist(self):
        self.playlist = self.playlists_tree.selected_playlist
        self.on_update(state=PlaylistState.EDITING,
                       playlist_name=self.playlist)

    def cancel_playlist(self):
        self.playlist = self.playlists_tree.selected_playlist
        self.on_update(state=PlaylistState.VIEWING,
                       playlist_name=self.playlist)

    def add_playlist(self):
        playlist_name = self.toolbar.editing_playlist
        if not self._is_alphanumeric(playlist_name):
            self.show_dialog(
                title="Alert",
                message="A playlist name must contain only letters, \n "
                "numbers, underscores, or spaces.",
                dialog_type=toga.InfoDialog  # type: ignore
            )
            return
        # Save the settings
        if not self.settings.has_playlist(playlist_name):
            self.settings.add_playlist(playlist_name)
            self.settings.save()
            self.on_update(state=PlaylistState.VIEWING,
                           playlist_name=self.playlist)
        else:
            self.show_dialog(
                title="Alert",
                message=f"A playlist with the same name '{playlist_name}'"
                " already exists.",
                dialog_type=toga.InfoDialog  # type: ignore
            )

    def remove_playlist(self):
        playlist_name = self.playlists_tree.selected_playlist
        if self.settings.has_playlist(playlist_name):
            playlist = self.settings.find_playlist(playlist_name)
            if len(playlist.tracks) > 0:
                def callback(task):
                    if task.result():
                        self.settings.remove_playlist(playlist_name,
                                                      self.ml_app.data_path)
                        self.settings.save()
                        self.on_update(state=PlaylistState.VIEWING,
                                       playlist_name=self.playlist)

                self.show_dialog(
                    title="Delete",
                    message="Are you sure you want to delete the playlist with saved track?",
                    dialog_type=toga.ConfirmDialog,  # type: ignore
                    dialog_callback=callback
                )
                return

            self.settings.remove_playlist(playlist_name,
                                          self.ml_app.data_path)
            self.settings.save()
            self.on_update(state=PlaylistState.VIEWING,
                           playlist_name=self.playlist)

    def edit_playlist(self):
        new_playlist_name = self.toolbar.editing_playlist
        if not self._is_alphanumeric(new_playlist_name):
            self.show_dialog(
                title="Alert",
                message="A playlist name must contain only letters, \n"
                "numbers, underscores, or spaces.",
                dialog_type=toga.InfoDialog  # type: ignore
            )
            return

        if not self.settings.has_playlist(new_playlist_name):
            playlist_name = self.playlists_tree.selected_playlist  # type: ignore
            self.settings.edit_playlist(playlist_name,
                                        new_playlist_name,
                                        self.ml_app.data_path)
            self.settings.save()
            self.on_update(state=PlaylistState.VIEWING,
                           playlist_name=self.playlist)
        else:
            if self.playlists_tree.selected_playlist == new_playlist_name:
                self.on_update(state=PlaylistState.VIEWING,
                               playlist_name=self.playlist)
            else:
                self.show_dialog(
                    title="Alert",
                    message=f"A playlist with the same name '{new_playlist_name}'"
                    " already exists.",
                    dialog_type=toga.InfoDialog  # type: ignore
                )

    def view_play_deck(self):
        tree = self.playlists_tree  # type: ignore
        if tree.playlists_list.selection is None:  # type: ignore
            self.show_dialog(
                title="Alert",
                message="Please select a playlist for playing.",
                dialog_type=toga.InfoDialog  # type: ignore
            )
            return
        # Get the selected playlist
        playlist_name = tree.playlists_list.selection.name  # type: ignore
        self.ml_app.show_player(playlist_name)  # type: ignore

    def _is_alphanumeric(self, playlist_name: str) -> bool:
        return bool(re.match(r'^[a-zA-Z0-9_ ]+$', playlist_name))
