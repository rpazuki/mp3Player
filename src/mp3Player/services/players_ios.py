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
        self.player = None
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

            from rubicon.objc import ObjCClass, objc_const
            from rubicon.objc.runtime import load_library
            _ = load_library("AVFoundation")
            avfAudio_lib = load_library("AVFAudio")
            AVAudioPlayer = ObjCClass('AVAudioPlayer')
            AVAudioSession = ObjCClass('AVAudioSession')
            NSURL = ObjCClass('NSURL')
            #
            AVAudioSessionCategoryPlayback = objc_const(avfAudio_lib, "AVAudioSessionCategoryPlayback")
            audioSession = AVAudioSession.sharedInstance()
            audioSession.setCategory_error_(AVAudioSessionCategoryPlayback, None)
            #
            audio_url = NSURL.fileURLWithPath_(  # type: ignore
                str(self.mp3.data_path))
            self.player = AVAudioPlayer.alloc().initWithContentsOfURL_error_(audio_url,  # type: ignore
                                                                        None)            
            if self.player and self.player.prepareToPlay():
                self.player.play()
            else:
                log.error("Failed to prepare audio player.")
                if (self.end_callback and
                        PlayingThreadGlobals.status == PlayerStatus.PLAY):
                    self.end_callback()  # type: ignore
                return

            PlayingThreadGlobals.played_secs = self.player.currentTime
            PlayingThreadGlobals.remained_secs = self.player.duration - self.player.currentTime
            # while success and not stop:
            c = 0
            while (self.player.isPlaying() and
                   PlayingThreadGlobals.status != PlayerStatus.STOP):
                PlayingThreadGlobals.played_secs = self.player.currentTime
                PlayingThreadGlobals.remained_secs = self.player.duration - self.player.currentTime
                time.sleep(0.1)
            

                while PlayingThreadGlobals.status == PlayerStatus.PAUSE:
                    self.player.pause()
                    time.sleep(0.1)
                    if PlayingThreadGlobals.status != PlayerStatus.PAUSE:
                        self.player.play()
            self.player.stop()
            if (self.end_callback and
                    PlayingThreadGlobals.status == PlayerStatus.PLAY):
                self.end_callback()  # type: ignore

        except RuntimeError as e:
            log.error("PlayThread:run: Could not read stream. %s" % e)

        finally:
            pass
