"""
Studying bees diseases by analysing photos
"""
import logging
import platform

from pyMOSF.toga import TogaMultiLayoutApp

from mp3Player.toga.configs import Settings
from mp3Player.toga.player_layouts import DesktopPlayerLayout, IOSPlayerLayout
from mp3Player.toga.playlist_layouts import (
    DesktopPlaylistLayout,
    IOSPlaylistLayout,
    PlaylistState,
)

log = logging.getLogger(__name__)


class TogaApp(TogaMultiLayoutApp):
    """A toga App class that has a layout.

    The layout class will create UI elements and its main_box will be added
    as the app main window's content.
    """

    def __init__(self,
                 formal_name: str,
                 app_id="net.pazuki.mp3player"):

        self._playlist_layout = self._new_playlist_layout()
        self._player_layout = self._new_player_layout()
        super(TogaApp, self).__init__(init_layout=self._playlist_layout,
                                      formal_name=formal_name,
                                      app_id=app_id,
                                      )

    def _new_player_layout(self):
        os = self._get_platform()
        match os:
            case "linux" | "darwin" | "windows":
                return DesktopPlayerLayout(self)
            case "ios" | "ipados":
                return IOSPlayerLayout(self)
            case _:
                raise NotImplementedError(f"OS {os} is not supported")

    def _new_playlist_layout(self):
        os = self._get_platform()
        match os:
            case "linux" | "darwin" | "windows":
                return DesktopPlaylistLayout(self)
            case "ios" | "ipados":
                return IOSPlaylistLayout(self)
            case _:
                raise NotImplementedError(f"OS {os} is not supported")

    def startup(self):
        super().startup()
        # If the last playlist is empty, show the last playlist instead of
        # PlaylistLayout
        self._settings = Settings.load(self.data_path)

        if (self.settings.last_playlist_private != "" and
                self.settings.find_playlist(self.settings.last_playlist_private)):
            self.show_player(self.settings.last_playlist_private)
        else:
            self._playlist_layout.on_update(state=PlaylistState.LOADING,
                                            playlist_name=self._playlist_layout.playlist)

    def show_player(self, playlist_name):
        self._player_layout.audio.playlist_name = playlist_name
        playlist = self._settings.find_playlist(playlist_name)
        if playlist and len(playlist.tracks) > 0:
            self._player_layout.audio.index = 0
            self._player_layout.files_list.selected_index = 0

        self.show_layout(self._player_layout)

    def show_playlists(self):
        self.show_layout(self._playlist_layout)

    def _get_platform(self):
        return platform.system().lower()


def create_app():
    log.info("mp3Player app stars")

    app = TogaApp("mp3 Player")
    return app


if __name__ == "__main__":
    log.info("Debug main is called.")
    try:
        create_app().main_loop()
    except Exception as e:
        print(e)
        log.error("Exception in main loop. \n"
                  f"Exception: {e}"
                  f"\nTraceback: {e.__traceback__}")
