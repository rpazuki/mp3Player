import asyncio
import logging
import re
from enum import Enum

import toga
from pyMOSF.toga import TogaComponent, TogaMultiLayoutApp, TogaStackedLayout

log = logging.getLogger(__name__)


class PlaylistState(int, Enum):
    VIEWING = 0
    ADDING = 1
    REMOVING = 2
    EDITING = 3
    SELECTING = 4
    LOADING = 5


class CommonPlaylistToolbarComponent(TogaComponent):
    def __init__(self,
                 layout: TogaStackedLayout,
                 playlist_textbox: toga.TextInput,
                 **kwargs) -> None:

        self.playlist_textbox = playlist_textbox
        super().__init__(layout, **kwargs)

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


class CommonPlaylistLayout(TogaStackedLayout):
    def __init__(self, app: TogaMultiLayoutApp, *types):
        super().__init__(app, *types)
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

    def on_load(self):
        # Load the list of playlists
        self.on_update(state=PlaylistState.LOADING,
                       playlist_name=self.playlist)
        return super().on_load()

    # Only called in Desktop version
    def playlist_selected(self):
        self.playlist = self.playlists_tree.selected_playlist  # type: ignore
        self.toolbar.on_update(state=PlaylistState.SELECTING,  # type: ignore
                               playlist_name=self.playlist)

    def show_add_playlist(self):
        self.playlist = ""
        self.on_update(state=PlaylistState.ADDING,
                       playlist_name=self.playlist)

    def show_edit_playlist(self):
        self.playlist = self.playlists_tree.selected_playlist  # type: ignore
        self.on_update(state=PlaylistState.EDITING,
                       playlist_name=self.playlist)

    def cancel_playlist(self):
        self.playlist = self.playlists_tree.selected_playlist  # type: ignore
        self.on_update(state=PlaylistState.VIEWING,
                       playlist_name=self.playlist)

    def add_playlist(self):
        playlist_name = self.toolbar.editing_playlist  # type: ignore
        if not self._is_alphanumeric(playlist_name):
            self.show_dialog(
                title="Alert",
                message="A playlist name must contain only letters, \n "
                "numbers, underscores, or spaces.",
                dialog_type=toga.InfoDialog  # type: ignore
            )
            return
        # Save the settings
        if not self.ml_app.settings.has_playlist(playlist_name):
            self.ml_app.settings.add_playlist(playlist_name)
            self.ml_app.settings.save()
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
        playlist_name = self.playlists_tree.selected_playlist  # type: ignore
        if self.ml_app.settings.has_playlist(playlist_name):
            playlist = self.ml_app.settings.find_playlist(playlist_name)
            if len(playlist.tracks) > 0:
                def callback(task):
                    if task.result():
                        self.ml_app.settings.remove_playlist(playlist_name,
                                                             self.ml_app.data_path)
                        self.ml_app.settings.save()
                        self.on_update(state=PlaylistState.VIEWING,
                                       playlist_name=self.playlist)

                self.show_dialog(
                    title="Delete",
                    message="Are you sure you want to delete the playlist with saved track?",
                    dialog_type=toga.ConfirmDialog,  # type: ignore
                    dialog_callback=callback
                )
                return

            self.ml_app.settings.remove_playlist(playlist_name,
                                                 self.ml_app.data_path)
            self.ml_app.settings.save()
            self.on_update(state=PlaylistState.VIEWING,
                           playlist_name=self.playlist)

    def edit_playlist(self):
        new_playlist_name = self.toolbar.editing_playlist  # type: ignore
        if not self._is_alphanumeric(new_playlist_name):
            self.show_dialog(
                title="Alert",
                message="A playlist name must contain only letters, \n"
                "numbers, underscores, or spaces.",
                dialog_type=toga.InfoDialog  # type: ignore
            )
            return

        if not self.ml_app.settings.has_playlist(new_playlist_name):
            playlist_name = self.playlists_tree.selected_playlist  # type: ignore
            self.ml_app.settings.edit_playlist(playlist_name,
                                               new_playlist_name,
                                               self.ml_app.data_path)
            self.ml_app.settings.save()
            self.on_update(state=PlaylistState.VIEWING,
                           playlist_name=self.playlist)
        else:
            if self.playlists_tree.selected_playlist == new_playlist_name:  # type: ignore
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
