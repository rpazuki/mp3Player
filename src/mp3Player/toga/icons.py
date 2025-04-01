
from pathlib import Path

import toga


class Icons:

    # https://www.iconarchive.com/show/farm-fresh-icons-by-fatcow.1.html
    _instance = None
    _data_path = Path(__file__).parent.parent / "resources"
    add = None
    add_package = None
    book = None
    cd = None
    cd_case = None
    cross = None
    column = None
    delete = None
    drawer = None
    edit = None
    forward = None
    mp2 = None
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

    @staticmethod
    def load():
        """Load the icons from the data path."""
        if Icons._instance is None:
            Icons._instance = Icons()
            # Load icons here
            Icons._instance.add = toga.Icon(Icons._data_path / "Add.32.png")
            Icons._instance.add_package = toga.Icon(
                Icons._data_path / "Add-package.32.png")
            Icons._instance.book = toga.Icon(Icons._data_path / "Book.32.png")
            Icons._instance.column = toga.Icon(
                Icons._data_path / "Column.32.png")
            Icons._instance.delete = toga.Icon(
                Icons._data_path / "Delete.32.png")
            Icons._instance.cd = toga.Icon(Icons._data_path / "Cd.32.png")
            Icons._instance.cd_case = toga.Icon(
                Icons._data_path / "Cd-case.32.png")
            Icons._instance.cross = toga.Icon(
                Icons._data_path / "Cross.32.png")
            Icons._instance.drawer = toga.Icon(
                Icons._data_path / "Drawer.32.png")
            Icons._instance.edit = toga.Icon(Icons._data_path / "Edit.32.png")
            Icons._instance.forward = toga.Icon(
                Icons._data_path / "Forward.32.png")
            Icons._instance.mp2 = toga.Icon(Icons._data_path / "Mp2.32.png")
            Icons._instance.nosound = toga.Icon(
                Icons._data_path / "Nosound.32.png")
            Icons._instance.pause = toga.Icon(
                Icons._data_path / "Pause.32.png")
            Icons._instance.pencil = toga.Icon(
                Icons._data_path / "Pencil.32.png")
            Icons._instance.play = toga.Icon(Icons._data_path / "Play.32.png")
            Icons._instance.plus = toga.Icon(Icons._data_path / "Plus.32.png")
            Icons._instance.recover = toga.Icon(
                Icons._data_path / "Recover.32.png")
            Icons._instance.rewind = toga.Icon(
                Icons._data_path / "Rewind.32.png")
            Icons._instance.reject = toga.Icon(
                Icons._data_path / "Reject.32.png")
            Icons._instance.report = toga.Icon(
                Icons._data_path / "Report.32.png")
            Icons._instance.report_add = toga.Icon(
                Icons._data_path / "Report_add.32.png")
            Icons._instance.report_delete = toga.Icon(
                Icons._data_path / "Report_delete.32.png")
            Icons._instance.report_edit = toga.Icon(
                Icons._data_path / "Report_edit.32.png")
            Icons._instance.report_go = toga.Icon(
                Icons._data_path / "Report_go.32.png")
            Icons._instance.report_save = toga.Icon(
                Icons._data_path / "Report_save.32.png")
            Icons._instance.report_stack = toga.Icon(
                Icons._data_path / "Report_stack.32.png")
            Icons._instance.sound = toga.Icon(
                Icons._data_path / "Sound.32.png")
            Icons._instance.stop = toga.Icon(Icons._data_path / "Stop.32.png")
            Icons._instance.tick = toga.Icon(Icons._data_path / "Tick.32.png")
            Icons._instance.trash = toga.Icon(
                Icons._data_path / "Trash.32.png")
            Icons._instance.wishlist_add = toga.Icon(
                Icons._data_path / "Wishlist_add.32.png")

        return Icons._instance
