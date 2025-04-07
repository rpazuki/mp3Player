import logging
import threading
import time

from mp3Player.services.players_core import PlayerStatus, PlayingThreadGlobals

log = logging.getLogger(__name__)


class IOSPlayerThread(threading.Thread):
    """A separate thread for music player."""
    CHUNK = 1024

    def __init__(self, mp3, end_callback=None):
        threading.Thread.__init__(self)
        self.mp3 = mp3
        # self.decoder = mp3.decoder()
        self.end_callback = end_callback
        #

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
            # from ctypes import byref, c_void_p, pointer

            from rubicon.objc import ObjCClass
            from rubicon.objc.runtime import load_library
            _ = load_library("AVFoundation")
            AVAudioPlayer = ObjCClass('AVAudioPlayer')
            NSURL = ObjCClass('NSURL')
            #
            audio_url = NSURL.fileURLWithPath_(  # type: ignore
                str(self.mp3.data_path))
            player = AVAudioPlayer.alloc().initWithContentsOfURL_error_(audio_url,  # type: ignore
                                                                        None)            
            if player and player.prepareToPlay():
                player.play()
            else:
                log.error("Failed to prepare audio player.")
                if (self.end_callback and
                        PlayingThreadGlobals.status == PlayerStatus.PLAY):
                    self.end_callback()  # type: ignore
                return

            PlayingThreadGlobals.played_secs = player.currentTime
            PlayingThreadGlobals.remained_secs = player.duration - player.currentTime
            # while success and not stop:
            while (player.isPlaying and
                   PlayingThreadGlobals.status != PlayerStatus.STOP):
                PlayingThreadGlobals.played_secs = player.currentTime
                PlayingThreadGlobals.remained_secs = player.duration - player.currentTime
                time.sleep(0.1)

                while PlayingThreadGlobals.status == PlayerStatus.PAUSE:
                    player.pause()
                    time.sleep(0.1)
                    if PlayingThreadGlobals.status != PlayerStatus.PAUSE:
                        player.play()

            if (self.end_callback and
                    PlayingThreadGlobals.status == PlayerStatus.PLAY):
                self.end_callback()  # type: ignore

        except RuntimeError as e:
            log.error("PlayThread:run: Could not read stream. %s" % e)

        finally:
            pass
