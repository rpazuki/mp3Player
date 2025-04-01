import asyncio
import logging

import toga

# , silence_crossed_events
from toga.style import Pack
from toga.style.pack import CENTER, COLUMN, ROW  # type: ignore

from mp3Player.toga import TogaComponent, TogaMultiLayoutApp, TogaStackedLayout
from mp3Player.toga.icons import Icons

log = logging.getLogger(__name__)


class PlaylistToolbarComponent(TogaComponent):
    def __init__(self, layout: TogaStackedLayout, **kwargs) -> None:
        icons = Icons.load()
        icon_style = Pack(width=48, height=48)
        buttons_box = toga.Box(style=Pack(direction=ROW, alignment=CENTER),
                               children=[
            toga.Button(icon=icons.cd_case,
                        on_press=self.view_play_deck,
                        style=icon_style),
            toga.Button(icon=icons.report_add,
                        on_press=self.add_playlist,
                        style=icon_style),
            toga.Button(icon=icons.report_delete,
                        on_press=self.remove_playlist,
                        enabled=False,
                        style=icon_style),
            toga.Button(icon=icons.report_edit,
                        on_press=self.edit_playlist,
                        enabled=False,
                        style=icon_style),
        ])
        edit_box = toga.Box(style=Pack(direction=ROW, alignment=CENTER),
                            children=[
            toga.TextInput("", readonly=True,),
            toga.Button(icon=icons.tick,
                        on_press=self.accept_playlist,
                        enabled=False,
                        style=icon_style),
            toga.Button(icon=icons.cross,
                        on_press=self.reject_playlist,
                        enabled=False,
                        style=icon_style),
        ]
        )
        self.btn_remove_playlist = buttons_box.children[2]  # type: ignore
        self.btn_edit_playlist = buttons_box.children[3]  # type: ignore

        self.playlist_textbox = edit_box.children[0]  # type: ignore
        self.btn_ok = edit_box.children[1]  # type: ignore
        self.btn_cancel = edit_box.children[2]  # type: ignore
        super().__init__(layout, style=Pack(
            direction=ROW, alignment=CENTER, padding=1),
            children=[
                toga.Box(style=Pack(direction=COLUMN, alignment=CENTER),
                         children=[
                             buttons_box,
                             edit_box,
                ]),
        ])

    def enable(self, flg):
        if flg:
            self.btn_ok.enabled = True
            self.btn_cancel.enabled = True
            self.playlist_textbox.readonly = False
        else:
            self.btn_ok.enabled = False
            self.btn_cancel.enabled = False
            self.playlist_textbox.readonly = True

    def reset(self):
        self.enable(False)
        self.playlist_textbox.value = ""
        self.btn_remove_playlist.enabled = False
        self.btn_edit_playlist.enabled = False

    def view_play_deck(self, widget):
        tree = self.parent_layout.playlists_tree  # type: ignore
        if tree.playlists_list.selection is None:  # type: ignore
            return
        # Get the selected playlist
        # playlist_name = self.playlist_textbox.value
        playlist_name = tree.playlists_list.selection.name  # type: ignore
        self.parent_layout.ml_app.show_main(playlist_name)  # type: ignore

    def add_playlist(self, widget):
        self.editing = False
        self.playlist_textbox.value = ""
        self.enable(True)

    def remove_playlist(self, widget):
        self.enable(False)
        playlist_name = self.playlist_textbox.value
        if playlist_name == "":
            return

        self.parent_layout.remove_playlist(playlist_name)  # type: ignore
        self.parent_layout[PlaylistsListComponent].load_playlists()

    def edit_playlist(self, widget):
        self.editing = True
        self.enable(True)

    def accept_playlist(self, widget):
        self.enable(False)
        playlist_name = self.playlist_textbox.value
        if playlist_name == "":
            return
        if self.editing:
            self.parent_layout.edit_playlist(playlist_name)  # type: ignore
        else:  # adding
            self.parent_layout.add_playlist(playlist_name)  # type: ignore
        self.parent_layout[PlaylistsListComponent].load_playlists()

    def reject_playlist(self, widget):
        self.enable(False)

    def selected_playlist(self, playlist_name):
        # Get the selected playlist
        self.playlist_textbox.value = playlist_name
        self.btn_remove_playlist.enabled = True
        self.btn_edit_playlist.enabled = True


class PlaylistsListComponent(TogaComponent):
    def __init__(self, layout: TogaStackedLayout, **kwargs) -> None:
        self.__playlists = toga.DetailedList(accessors=("name", "file_number", "picture"),
                                             style=Pack(flex=1),
                                             on_select=self.on_select,
                                             )
        super().__init__(layout, style=Pack(padding=10, flex=1),
                         children=[self.__playlists])

    @property
    def playlists_list(self) -> toga.DetailedList:
        return self.__playlists

    def load_playlists(self):
        ############
        # Settings
        self.settings = self.ml_app.settings
        #
        self.playlists_list.data.clear()
        for playlist in self.settings.Playlists:
            self.playlists_list.data.append({
                "picture": Icons.load().column,
                "name": playlist.name,
                "file_number": len(playlist.tracks),
            })

    def on_select(self, widget):
        if self.playlists_list.selection is None:
            return
        playlist_name = self.playlists_list.selection.name  # type: ignore
        self.parent_layout[PlaylistToolbarComponent].selected_playlist(
            playlist_name)  # type: ignore

    def add_playlist_to_tree(self, playlist_name):
        self.playlists_list.data.append({
            "picture": Icons.load().column,
            "name": playlist_name,
            "file_number": 0
        })

    def remove_track_from_playlist_tree(self, tree_node):
        self.playlists_list.data.remove(tree_node)


class PlaylistLayout(TogaStackedLayout):
    def __init__(self, app: TogaMultiLayoutApp):
        super().__init__(app,
                         PlaylistToolbarComponent,
                         PlaylistsListComponent)

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
        self.playlists_tree.load_playlists()
        self.toolbar.reset()
        return super().on_load()

    def add_playlist(self, playlist_name):
        # Save the settings
        if not self.settings.has_playlist(playlist_name):
            self.settings.add_playlist(playlist_name)
            self.settings.save()

    def remove_playlist(self, playlist_name):
        if self.settings.has_playlist(playlist_name):
            playlist = self.settings.find_playlist(playlist_name)
            if len(playlist.tracks) > 0:
                confirm = toga.ConfirmDialog(
                    "Delete",
                    "Are you sure you want to delete the playlist with saved track?"
                )
                task = asyncio.create_task(
                    self.ml_app.main_window.dialog(confirm))  # type: ignore

                def callback(task):
                    if task.result():
                        self.settings.remove_playlist(playlist_name,
                                                      self.ml_app.data_path)
                        self.settings.save()
                        self[PlaylistsListComponent].load_playlists()

                task.add_done_callback(callback)
                return

            self.settings.remove_playlist(playlist_name,
                                          self.ml_app.data_path)
            self.settings.save()

    def edit_playlist(self, new_playlist_name):
        if not self.settings.has_playlist(new_playlist_name):
            playlist_name = self.playlists_tree.playlists_list.selection.name  # type: ignore
            self.settings.edit_playlist(playlist_name,
                                        new_playlist_name,
                                        self.ml_app.data_path)
            self.settings.save()
