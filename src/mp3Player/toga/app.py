"""
Studying bees diseases by analysing photos
"""
import logging
import platform

from pyMOSF.toga import TogaMultiLayoutApp

from mp3Player.services import PlayerStatus, PlayingThreadGlobals
from mp3Player.toga.configs import Settings
from mp3Player.toga.player_layouts import DesktopPlayerLayout, IOSPlayerLayout
from mp3Player.toga.playlist_layouts import DesktopPlaylistLayout, IOSPlaylistLayout

log = logging.getLogger(__name__)


class TogaApp(TogaMultiLayoutApp):
    """A toga App class that has a layout.

    The layout class will create UI elements and its main_box will be added
    as the app main window's content.
    """

    def __init__(self,
                 formal_name: str,
                 app_id="net.pazuki.mp3player"):

        os = self._get_platform()
        match os:
            case "linux" | "darwin" | "windows":
                self.player_layout = DesktopPlayerLayout(self)
                self.playlist_layout = DesktopPlaylistLayout(self)
            case "ios" | "ipados":
                self.player_layout = IOSPlayerLayout(self)
                self.playlist_layout = IOSPlaylistLayout(self)
            case _:
                raise NotImplementedError(f"OS {os} is not supported")

        super(TogaApp, self).__init__(init_layout=self.playlist_layout,
                                      formal_name=formal_name,
                                      app_id=app_id,
                                      )

    def startup(self):
        super().startup()
        # If the last playlist is empty, show the last playlist instead of
        # PlaylistLayout
        self._settings = Settings.load(self.data_path)

        if (self.settings.last_playlist_private != "" and
                self.settings.find_playlist(self.settings.last_playlist_private)):
            self.show_player(self.settings.last_playlist_private)

    def show_player(self, playlist_name):
        self.player_layout.audio.playlist_name = playlist_name
        self.show_layout(self.player_layout)

    def show_playlists(self):
        PlayingThreadGlobals.status = PlayerStatus.STOP
        if self.player_layout.player_thread is not None:
            try:
                self.player_layout.progress_thread.join()
                self.player_layout.player_thread.join()
            except RuntimeError:
                pass
        self.show_layout(self.playlist_layout)

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
