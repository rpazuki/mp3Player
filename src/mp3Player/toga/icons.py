
from pathlib import Path

import toga


class Icons:

    # https://www.iconarchive.com/show/farm-fresh-icons-by-fatcow.1.html
    # https://www.iconarchive.com/show/button-icons-by-hopstarter.html
    # https://www.iconarchive.com/show/soft-scraps-icons-by-hopstarter.1.html
    # https://www.iconarchive.com/show/oxygen-icons-by-oxygen-icons.org/Status-audio-volume-muted-icon.html
    # https://www.iconarchive.com/show/nuoveXT-icons-by-saki.1.html
    _instance = None
    _data_path = Path(__file__).parent.parent / "resources"
    add = None
    add_package = None
    book = None
    cd = None
    cd_case = None
    close = None
    cross = None
    column = None
    delete = None
    drawer = None
    edit = None
    forward = None
    mp2 = None
    mp3 = None
    mp3_player = None
    nosound = None
    pause = None
    pencil = None
    play = None
    plus = None
    recover = None
    rewind = None
    reject = None
    report = None
    report_add = None
    report_delete = None
    report_edit = None
    report_go = None
    report_save = None
    report_stack = None
    sound = None
    stop = None
    tick = None
    trash = None
    wishlist_add = None

    mp3_sample = None
    mp3_sample_2 = None

    @staticmethod
    def load():
        """Load the icons from the data path."""
        if Icons._instance is None:
            Icons._instance = Icons()
            # Load icons here
            Icons._instance.add = toga.Icon(Icons._data_path / "Add.256.png")
            Icons._instance.add_package = toga.Icon(
                Icons._data_path / "Add-package.32.png")
            Icons._instance.book = toga.Icon(Icons._data_path / "Book.256.png")
            Icons._instance.column = toga.Icon(
                Icons._data_path / "Column.32.png")
            Icons._instance.close = toga.Icon(
                Icons._data_path / "Close.256.png")
            Icons._instance.delete = toga.Icon(
                Icons._data_path / "Delete.256.png")
            Icons._instance.cd = toga.Icon(Icons._data_path / "Cd.32.png")
            Icons._instance.cd_case = toga.Icon(
                Icons._data_path / "Cd-case.32.png")
            Icons._instance.cross = toga.Icon(
                Icons._data_path / "Cross.256.png")
            Icons._instance.drawer = toga.Icon(
                Icons._data_path / "Drawer.32.png")
            Icons._instance.edit = toga.Icon(Icons._data_path / "Edit.32.png")
            Icons._instance.forward = toga.Icon(
                Icons._data_path / "Forward.256.png")
            Icons._instance.mp2 = toga.Icon(Icons._data_path / "Mp2.32.png")
            Icons._instance.mp3 = toga.Icon(Icons._data_path / "Mp3.256.png")
            Icons._instance.mp3_player = toga.Icon(Icons._data_path / "Mp3Player.128.png")
            Icons._instance.nosound = toga.Icon(
                Icons._data_path / "Nosound.256.png")
            Icons._instance.pause = toga.Icon(
                Icons._data_path / "Pause.256.png")
            Icons._instance.pencil = toga.Icon(
                Icons._data_path / "Pencil.32.png")
            Icons._instance.play = toga.Icon(Icons._data_path / "Play.256.png")
            Icons._instance.plus = toga.Icon(Icons._data_path / "Plus.32.png")
            Icons._instance.recover = toga.Icon(
                Icons._data_path / "Recover.32.png")
            Icons._instance.rewind = toga.Icon(
                Icons._data_path / "Rewind.256.png")
            Icons._instance.reject = toga.Icon(
                Icons._data_path / "Reject.32.png")
            Icons._instance.report = toga.Icon(
                Icons._data_path / "Report.128.png")
            Icons._instance.report_add = toga.Icon(
                Icons._data_path / "Report_add.256.png")
            Icons._instance.report_delete = toga.Icon(
                Icons._data_path / "Report_delete.256.png")
            Icons._instance.report_edit = toga.Icon(
                Icons._data_path / "Report_edit.256.png")
            Icons._instance.report_go = toga.Icon(
                Icons._data_path / "Report_go.32.png")
            Icons._instance.report_save = toga.Icon(
                Icons._data_path / "Report_save.32.png")
            Icons._instance.report_stack = toga.Icon(
                Icons._data_path / "Report_stack.32.png")
            Icons._instance.sound = toga.Icon(
                Icons._data_path / "Sound.256.png")
            Icons._instance.stop = toga.Icon(Icons._data_path / "Stop.256.png")
            Icons._instance.tick = toga.Icon(Icons._data_path / "Tick.256.png")
            Icons._instance.trash = toga.Icon(
                Icons._data_path / "Trash.32.png")
            Icons._instance.wishlist_add = toga.Icon(
                Icons._data_path / "Wishlist_add.32.png")
            #
            Icons._instance.mp3_sample = Icons._data_path / "file_example_MP3_700KB.mp3"
            Icons._instance.mp3_sample_2 = Icons._data_path / "sample-15s.mp3"

        return Icons._instance
