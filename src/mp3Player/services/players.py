
import logging
import threading
import time

from mp3Player.services.players_core import PlayerStatus, PlayingThreadGlobals

log = logging.getLogger(__name__)


class PlayerThread(threading.Thread):
    """A separate thread for music player."""
    CHUNK = 1024

    def __init__(self, mp3, end_callback=None):
        threading.Thread.__init__(self)
        import pyaudio
        self.mp3 = mp3
        self.decoder = mp3.decoder()
        self.pAudio = pyaudio.PyAudio()
        self.end_callback = end_callback

    def get_format(self):
        """Get the format of the audio stream."""
        import mp3 as mp3_lib
        match self.decoder.get_mode():
            case mp3_lib.MODE_SINGLE_CHANNEL:
                return mp3_lib.MODE_SINGLE_CHANNEL
            case mp3_lib.MODE_DUAL_CHANNEL:
                return mp3_lib.MODE_STEREO
            case mp3_lib.MODE_JOINT_STEREO:
                return mp3_lib.MODE_JOINT_STEREO
            case _:
                return mp3_lib.MODE_JOINT_STEREO

    def run(self):
        """
        Executes the audio playback process using the decoder and PyAudio.

        This method initializes an audio stream with the appropriate format,
        channels, and sample rate based on the decoder's configuration. It
        continuously reads chunks of audio data from the decoder and writes
        them to the audio stream for playback, as long as playback is enabled
        and there is data to read.

        If a runtime error occurs during the process, it logs an error message.

        Raises:
            RuntimeError: If there is an issue reading the audio stream.
        """
        try:

            format = self.pAudio.get_format_from_width(self.get_format())
            stream = self.pAudio.open(format=format,
                                      channels=self.decoder.get_channels(),
                                      rate=self.decoder.get_sample_rate(),
                                      output=True)

            total_seconds = self.mp3.audiofile.info.time_secs
            byte_per_second = (self.decoder.get_bit_rate() *
                               self.decoder.get_sample_rate() / 32.0)
            counter = 0
            PlayingThreadGlobals.played_secs = 0
            PlayingThreadGlobals.remained_secs = total_seconds
            # while success and not stop:
            while (len(data := self.decoder.read(PlayerThread.CHUNK)) and
                   PlayingThreadGlobals.status != PlayerStatus.STOP):
                counter += 1
                if counter % 10 == 0:
                    played_bytes = PlayerThread.CHUNK * counter
                    played_secs = played_bytes / byte_per_second
                    remained_seconds = total_seconds - played_secs
                    PlayingThreadGlobals.played_secs = played_secs
                    PlayingThreadGlobals.remained_secs = remained_seconds
                stream.write(data)
                while PlayingThreadGlobals.status == PlayerStatus.PAUSE:
                    time.sleep(0.1)

            if (self.end_callback and
                    PlayingThreadGlobals.status == PlayerStatus.PLAY):
                self.end_callback()  # type: ignore

        except RuntimeError as e:
            log.error("PlayThread:run: Could not read stream. %s" % e)

        finally:
            stream.close()
            self.pAudio.terminate()
