"""
Studying bees diseases by analysing photos
"""
import logging

# import mp3Player.core as core
# from mp3Player.core import ProcessesRegistry
from mp3Player.toga import TogaMultiLayoutApp
from mp3Player.toga.player_layouts import PlayerLayout
from mp3Player.toga.playlist_layouts import PlaylistLayout

log = logging.getLogger(__name__)


class TogaApp(TogaMultiLayoutApp):
    """A toga App class that has a layout.

    The layout class will create UI elements and its main_box will be added
    as the app main window's content.
    """

    def __init__(self,
                 formal_name: str,
                 app_id="net.pazuki.mp3player"):

        self.main_layout = PlayerLayout(self)
        super(TogaApp, self).__init__(init_layout=self.main_layout,
                                      formal_name=formal_name,
                                      app_id=app_id,
                                      )

    def show_main(self, playlist_name):
        self.main_layout.audio.playlist_name = playlist_name
        self.show_layout(self.main_layout)

    def show_playlists(self):
        self.main_layout.stop()
        if self.main_layout.player_thread is not None:
            try:
                self.main_layout.progress_thread.join()
                self.main_layout.player_thread.join()
            except RuntimeError:
                pass
        self.show_layout(PlaylistLayout(self))


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
