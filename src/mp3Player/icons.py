
from pathlib import Path

import toga


class Icons:

    # https://www.iconarchive.com/show/flatastic-2-icons-by-custom-icon-design.html
    # https://www.customicondesign.com/free-icons/
    _instance = None
    _data_path = Path(__file__).parent / "resources"
    add: toga.Icon | None = None
    address_book: toga.Icon | None = None
    address_book_add: toga.Icon | None = None
    cancel: toga.Icon | None = None
    delete: toga.Icon | None = None
    next: toga.Icon | None = None
    no_sound: toga.Icon | None = None
    note: toga.Icon | None = None
    mp3: toga.Icon | None = None
    music: toga.Icon | None = None
    pause: toga.Icon | None = None
    pencile: toga.Icon | None = None
    play: toga.Icon | None = None
    playlist_add: toga.Icon | None = None
    playlist_delete: toga.Icon | None = None
    playlist_edit: toga.Icon | None = None
    playlist_info: toga.Icon | None = None
    playlist: toga.Icon | None = None
    previous: toga.Icon | None = None
    stop: toga.Icon | None = None
    success: toga.Icon | None = None
    sound: toga.Icon | None = None

    mp3_sample = None
    mp3_sample_2 = None

    app_icon = None

    @staticmethod
    def load():
        """Load the icons from the data path."""
        if Icons._instance is None:
            Icons._instance = Icons()
            # Load icons here
            Icons._instance.add = toga.Icon(Icons._data_path / "add.png")
            Icons._instance.address_book = toga.Icon(
                Icons._data_path / "addressbook.png")
            Icons._instance.address_book_add = toga.Icon(
                Icons._data_path / "addressbook-add.png")
            Icons._instance.cancel = toga.Icon(Icons._data_path / "cancel.png")
            Icons._instance.delete = toga.Icon(Icons._data_path / "delete.png")
            Icons._instance.next = toga.Icon(Icons._data_path / "next.png")
            Icons._instance.no_sound = toga.Icon(
                Icons._data_path / "nosound.png")
            Icons._instance.note = toga.Icon(Icons._data_path / "note.png")
            Icons._instance.mp3 = toga.Icon(Icons._data_path / "mp3.png")
            Icons._instance.music = toga.Icon(Icons._data_path / "music.png")
            Icons._instance.pause = toga.Icon(Icons._data_path / "pause.png")
            Icons._instance.pencile = toga.Icon(
                Icons._data_path / "pencile.png")
            Icons._instance.play = toga.Icon(Icons._data_path / "play.png")
            Icons._instance.playlist_add = toga.Icon(
                Icons._data_path / "playlist-add.png")
            Icons._instance.playlist_delete = toga.Icon(
                Icons._data_path / "playlist-delete.png")
            Icons._instance.playlist_edit = toga.Icon(
                Icons._data_path / "playlist-edit.png")
            Icons._instance.playlist_info = toga.Icon(
                Icons._data_path / "playlist-info.png")
            Icons._instance.playlist = toga.Icon(
                Icons._data_path / "playlist.png")
            Icons._instance.previous = toga.Icon(
                Icons._data_path / "previous.png")
            Icons._instance.stop = toga.Icon(Icons._data_path / "stop.png")
            Icons._instance.success = toga.Icon(
                Icons._data_path / "success.png")
            Icons._instance.sound = toga.Icon(Icons._data_path / "sound.png")

            Icons._instance.app_icon = toga.Icon(
                Icons._data_path / "Mp3Player.128.png")

        return Icons._instance

    @staticmethod
    def get_app_icon() -> bytes:
        with open(Path(__file__).parent / "resources" / "Mp3Player.128.png", "rb") as f:
            data = f.read()
        return data
