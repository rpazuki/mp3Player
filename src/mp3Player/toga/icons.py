
from pathlib import Path

import toga


class Icons:

    # https://www.iconarchive.com/show/flatastic-2-icons-by-custom-icon-design.html
    # https://www.customicondesign.com/free-icons/
    _instance = None
    _data_path = Path(__file__).parent.parent / "resources"
    add = None
    cancel = None
    delete = None
    next = None
    no_sound = None
    note = None
    mp3 = None
    music = None
    pause = None
    pencile = None
    play = None
    playlist_add = None
    playlist_delete = None
    playlist_edit = None
    playlist_info = None
    playlist = None
    previous = None
    stop = None
    success = None
    sound = None

    mp3_sample = None
    mp3_sample_2 = None

    @staticmethod
    def load():
        """Load the icons from the data path."""
        if Icons._instance is None:
            Icons._instance = Icons()
            # Load icons here
            Icons._instance.add = toga.Icon(Icons._data_path / "add.png")
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

        return Icons._instance
