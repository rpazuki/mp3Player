import threading
import time
from enum import Enum


class PlayerStatus(int, Enum):
    STOP = 0
    PLAY = 1
    PAUSE = 2


class PlayingThreadGlobals:
    status = PlayerStatus.STOP
    played_secs = 0
    remained_secs = 1


lock_condition = threading.Condition()


class ProgressThread(threading.Thread):
    """A separate thread for updating player's progress bar."""

    def __init__(self, progress_callback=None):
        threading.Thread.__init__(self)
        self.progress_callback = progress_callback

    def run(self):
        while PlayingThreadGlobals.status != PlayerStatus.STOP:
            with lock_condition:
                lock_condition.wait(0.5)
                if self.progress_callback:
                    self.progress_callback(
                        PlayingThreadGlobals.played_secs,
                        PlayingThreadGlobals.remained_secs)
                while PlayingThreadGlobals.status == PlayerStatus.PAUSE:
                    time.sleep(0.1)
