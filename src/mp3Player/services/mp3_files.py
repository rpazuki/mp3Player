from __future__ import annotations

import shutil
from pathlib import Path

import eyed3
import mp3 as mp3_lib


class mp3:
    def __init__(self, audiofile, data_path: Path) -> None:
        self.audiofile = audiofile
        self._name = data_path.stem
        self._data_path = data_path

    @staticmethod
    def load(data_path: Path) -> mp3:
        """Load mp3 file and return the mp3 object."""
        audiofile = eyed3.load(data_path)
        if audiofile.tag is None:  # type: ignore
            audiofile.initTag()  # type: ignore
        return mp3(audiofile, data_path)

    def copy_to(self, dest_path: Path) -> None:
        """Copy mp3 file to the destination path."""
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        f_src = open(self.data_path, 'rb')
        f_dest = open(dest_path, 'wb')
        shutil.copyfileobj(f_src, f_dest)
        self._data_path = dest_path

    def delete(self) -> None:
        """Delete the mp3 file."""
        if self._data_path.exists():
            self._data_path.unlink()
        else:
            raise FileNotFoundError(f"File {self._data_path} not found.")

    @property
    def data_path(self) -> Path:
        """Return the path of the mp3 file."""
        return self._data_path

    def relative_path(self, playlist_name) -> Path:
        """Return the relative path of the mp3 file."""
        return Path("files") / playlist_name.replace(" ", "") / self.data_path.name

    @property
    def name(self) -> str:
        """Return the name of the mp3 file."""
        return self._name

    def decoder(self):
        read_file = open(self._data_path, 'rb')
        return mp3_lib.Decoder(read_file)

    @property
    def title(self) -> str:
        """Return the title of the mp3 file."""
        return self.audiofile.tag.title if self.audiofile.tag.title else ""

    @property
    def artist(self) -> str:
        """Return the artist of the mp3 file."""
        return self.audiofile.tag.artist if self.audiofile.tag.artist else ""

    @property
    def album(self) -> str:
        """Return the album of the mp3 file."""
        return self.audiofile.tag.album if self.audiofile.tag.album else ""

    @property
    def year(self) -> int:
        """Return the year of the mp3 file."""
        return self.audiofile.tag.release_date.year if self.audiofile.tag.release_date else 0

    @property
    def genre(self) -> str:
        """Return the genre of the mp3 file."""
        return self.audiofile.tag.genre.name if self.audiofile.tag.genre else ""

    @property
    def track_num(self) -> int:
        """Return the track number of the mp3 file."""
        return self.audiofile.tag.track_num[0] if self.audiofile.tag.track_num else 0

    @property
    def length(self) -> str:
        """Return the length of the mp3 file in seconds."""
        units = {"hours": 3600, "minutes": 60, "seconds": 1}
        values = []
        seconds = int(self.audiofile.info.time_secs)
        for unit, value in units.items():
            count = seconds // value
            seconds -= count * value
            values.append(count)
        return f"{values[0]:02d}:{values[1]:02d}:{values[2]:02d}"
