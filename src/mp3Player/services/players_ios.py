from __future__ import annotations

import io
import logging
import threading
import time

from rubicon.objc import (  # Block, at,
    NSMutableDictionary,
    ObjCClass,
    objc_block,
    objc_const,
    objc_method,
)
from rubicon.objc.runtime import load_library, objc_id
from rubicon.objc.types import CGSize

# from mp3Player.icons import Icons
from mp3Player.services.players_core import PlayerStatus, PlayingThreadGlobals

# , ctype_for_encoding, encoding_for_ctype


# from ctypes import c_void_p


log = logging.getLogger(__name__)

_ = load_library("AVFoundation")
_ = load_library('Foundation')
avfAudio_lib = load_library("AVFAudio")
libmp = load_library("MediaPlayer")
#
MPRemoteCommandHandlerStatusSuccess = 0  # objc_const(
#
UIApplication = ObjCClass("UIApplication")
MPRemoteCommandEvent = ObjCClass("MPRemoteCommandEvent")
MPRemoteCommand = ObjCClass("MPRemoteCommand")
AVAudioPlayer = ObjCClass('AVAudioPlayer')
AVAudioSession = ObjCClass('AVAudioSession')
NSObject = ObjCClass('NSObject')
NSURL = ObjCClass('NSURL')


MPNowPlayingInfoCenter = ObjCClass(
    'MPNowPlayingInfoCenter')  # type: ignore
MPRemoteCommandCenter = ObjCClass('MPRemoteCommandCenter')
MPMediaItemArtwork = ObjCClass("MPMediaItemArtwork")

AVAudioSessionCategoryPlayback = objc_const(avfAudio_lib,
                                            "AVAudioSessionCategoryPlayback")
MPMediaItemPropertyTitle = objc_const(libmp,
                                      "MPMediaItemPropertyTitle")
MPNowPlayingInfoPropertyElapsedPlaybackTime = objc_const(
    libmp,
    "MPNowPlayingInfoPropertyElapsedPlaybackTime")
MPMediaItemPropertyPlaybackDuration = objc_const(libmp,
                                                 "MPMediaItemPropertyPlaybackDuration")
MPNowPlayingInfoPropertyPlaybackRate = objc_const(libmp,
                                                  "MPNowPlayingInfoPropertyPlaybackRate")
MPMediaItemPropertyArtwork = objc_const(libmp,
                                        "MPMediaItemPropertyArtwork")


class MPMediaItemPropertyArtworkDelegate(NSObject):  # type: ignore

    @objc_method
    def init_(self):
        self = self.init()
        if self is None:
            return None
        self.image = None
        self.resize_method = None
        return self

    @objc_method
    def imageWithSize_(self, size: CGSize):
        # self.bounds = size
        return self.resize_method(size)  # type: ignore

    # @objc_method
    # def jpegDataWithSize_(self, size: CGSize):
    #     # self.bounds = size
    #     #message = NSString.stringWithString_("jpegDataWithSize_ is called")
    #     NSLog("jpegDataWithSize_ is called")
    #     return self.resize_method(size)  # type: ignore

    @objc_method
    def set_resize_method(self, resize_method: objc_block):
        self.resize_method = resize_method


class IOSPlayerThread(threading.Thread):
    """A separate thread for music player."""
    CHUNK = 1024

    def __init__(self, mp3, end_callback=None):
        threading.Thread.__init__(self)
        self.mp3 = mp3
        self.end_callback = end_callback
        self.player = None
        self.image_data = None
        #

    def resize_method_(self, size: CGSize) -> objc_id:
        from io import BytesIO

        from PIL import Image

        img = Image.open(BytesIO(self.image_data))  # type: ignore
        img = img.resize((int(size.width), int(size.height)))
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        # image = ObjCClass("UIImage").imageWithData_(  # type: ignore
        #    img_byte_arr)
        # image = ObjCClass("UIImage").alloc().initWithData_(  # type: ignore
        #    img_byte_arr)
        UIImage = ObjCClass("UIImage")
        nsdata = ObjCClass("NSData").dataWithBytes_length_(  # type: ignore
            img_byte_arr, len(img_byte_arr))
        ui_image = UIImage.alloc().initWithData_(nsdata)  # type: ignore

        return ui_image.ptr  # type: ignore

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
            # Create an audio session and set its category
            # to playback in background and allow mixing with other audio
            # sessions.
            # This is necessary for iOS to play audio in the background.
            audioSession = AVAudioSession.sharedInstance()  # type: ignore
            audioSession.setCategory_error_(
                AVAudioSessionCategoryPlayback, None)
            audioSession.setActive_error_(True, None)
            # create an audio player and prepare it for playback
            audio_url = NSURL.fileURLWithPath_(  # type: ignore
                str(self.mp3.data_path))
            self.player = AVAudioPlayer.alloc(  # type: ignore
            ).initWithContentsOfURL_error_(audio_url, None)
            if self.player and self.player.prepareToPlay():
                self.player.play()
            else:
                log.error("Failed to prepare audio player.")
                if (self.end_callback and
                        PlayingThreadGlobals.status == PlayerStatus.PLAY):
                    self.end_callback()  # type: ignore
                return
            # Set the Playing Center's info
            infos = NSMutableDictionary.dictionaryWithDictionary(  # type: ignore
                {})
            infos[MPMediaItemPropertyTitle] = self.mp3.name
            infos[MPNowPlayingInfoPropertyElapsedPlaybackTime] = self.player.currentTime
            infos[MPMediaItemPropertyPlaybackDuration] = self.player.duration
            infos[MPNowPlayingInfoPropertyPlaybackRate] = self.player.rate
            # if len(self.mp3.audiofile.tag.images) > 0:  # type: ignore
            #    self.image_data = self.mp3.audiofile.tag.images[0].image_data
            # else:
            #    self.image_data = Icons.get_app_icon()  # type: ignore

            # image = ObjCClass("UIImage").imageWithData_(  # type: ignore
            #                        self.image_data)
            # artwork = ObjCClass("MPMediaItemArtwork").alloc()
            # artwork = artwork.initWithBoundsSize_requestHandler_(
            #  image.size,
            #  self.resize_method_
            # )
            # infos[MPMediaItemPropertyArtwork] = artwork

            playingInfoCenter = MPNowPlayingInfoCenter.defaultCenter()  # type: ignore
            playingInfoCenter.nowPlayingInfo = infos
            #
            PlayingThreadGlobals.played_secs = self.player.currentTime
            PlayingThreadGlobals.remained_secs = self.player.duration - self.player.currentTime
            # while success and not stop:
            while (self.player and self.player.isPlaying() and
                   PlayingThreadGlobals.status != PlayerStatus.STOP):
                PlayingThreadGlobals.played_secs = self.player.currentTime
                PlayingThreadGlobals.remained_secs = self.player.duration - self.player.currentTime
                infos[MPNowPlayingInfoPropertyElapsedPlaybackTime] = self.player.currentTime
                playingInfoCenter.nowPlayingInfo = infos  # type: ignore
                time.sleep(0.1)

                while PlayingThreadGlobals.status == PlayerStatus.PAUSE:
                    self.player.pause()
                    infos[MPNowPlayingInfoPropertyPlaybackRate] = 0
                    playingInfoCenter.nowPlayingInfo = infos  # type: ignore
                    time.sleep(0.1)
                    if PlayingThreadGlobals.status != PlayerStatus.PAUSE:
                        self.player.play()
                        infos[MPNowPlayingInfoPropertyPlaybackRate] = 1
                        playingInfoCenter.nowPlayingInfo = infos  # type: ignore

            self.player.stop()
            if (self.end_callback and
                    PlayingThreadGlobals.status == PlayerStatus.PLAY):
                self.end_callback()  # type: ignore

        except RuntimeError as e:
            log.error("PlayThread:run: Could not read stream. %s" % e)

        finally:
            pass


class RemoteCommandCenter:
    """A class to handle remote command center events."""
    __instance = None

    @staticmethod
    def shared_instance() -> RemoteCommandCenter:
        if RemoteCommandCenter.__instance is None:
            RemoteCommandCenter.__instance = RemoteCommandCenter()
        return RemoteCommandCenter.__instance

    def __init__(self):

        self.play = None
        self.pause = None
        self.stop = None
        self.next = None
        self.previous = None
        self.command_center = MPRemoteCommandCenter.sharedCommandCenter()  # type: ignore
        self.application = UIApplication.sharedApplication  # type: ignore
        self.application.beginReceivingRemoteControlEvents()  # type: ignore

    def __command_factory(self, command, py_callback, *args):
        def local_callback(event: objc_id) -> int:  # type: ignore
            py_callback(*args)  # args, e.g., can be a widget
            return MPRemoteCommandHandlerStatusSuccess  # type: ignore
        #
        handler = local_callback
        command.enabled = True
        command.addTargetWithHandler_(handler)  # type: ignore

        return handler

    def play_command(self, callback, *args):
        if self.play is not None:
            raise RuntimeError("Play command already set.")
        self.play = self.__command_factory(self.command_center.playCommand,
                                           callback,
                                           *args)

    def pause_command(self, callback, *args):
        if self.pause is not None:
            raise RuntimeError("Pause command already set.")
        self.pause = self.__command_factory(self.command_center.pauseCommand,
                                            callback,
                                            *args)

    def stop_command(self, callback, *args):
        if self.stop is not None:
            raise RuntimeError("Stop command already set.")
        self.stop = self.__command_factory(self.command_center.stopCommand,
                                           callback,
                                           *args)

    def next_command(self, callback, *args):
        if self.next is not None:
            raise RuntimeError("Next command already set.")
        self.next = self.__command_factory(self.command_center.nextTrackCommand,
                                           callback,
                                           *args)

    def previous_command(self, callback, *args):
        if self.previous is not None:
            raise RuntimeError("Previous command already set.")
        self.previous = self.__command_factory(self.command_center.previousTrackCommand,
                                               callback,
                                               *args)
