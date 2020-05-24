from pydub import AudioSegment
from pydub.playback import play
import gpiozero
from signal import pause
import simpleaudio as sa
import time
import threading
import json
from rotator import Rotator
from sound import Sound

import faulthandler
faulthandler.enable()
PYTHONFAULTHANDLER = 1

class T65:
    HOOK_PIN_DEFAULT = 16
    DAILER_STEP_PIN_DEFAULT = 19
    DAILER_ISON_PIN_DEFAULT = 26

    __dailTone = None
    __playingMusic = None
    unhooked = False

    def run(self):
        with open('config.json') as json_file:
            self.config = json.load(json_file)

        self.__dailTone = Sound('./music/kiestoon-2s.wav')
        self.__dailTone.repeat = True

        self.rotator = Rotator(
            self.config.get('DialerRedGpio', self.DAILER_STEP_PIN_DEFAULT),
            self.config.get('DialerYellowGpio', self.DAILER_ISON_PIN_DEFAULT)
        )
        self.rotator.when_dailed = self.dailed

        self.hook = gpiozero.Button(self.config.get('HookGpio', self.HOOK_PIN_DEFAULT))
        self.hook.when_released = self.offHook
        self.hook.when_pressed = self.onHook

        print('t65 started')
        if not self.hook.is_pressed: # start offHook when it's already of the hook
            self.offHook()
        pause()

    def onHook(self):
        print('on hook')
        if self.__playingMusic: # stop music if playing
            self.__playingMusic.stop()
            del self.__playingMusic
        self.unhooked = False
        self.__dailTone.stop()

    def offHook(self):
        print('off hook')
        self.unhooked = True
        self.__dailTone.play()

    def dailed(self, number):
        if self.__playingMusic and self.__playingMusic.isPlaying(): # when song is playing
            return # do nothing
        
        if self.__dailTone.isPlaying():
            self.__dailTone.stop()

        # TODO: get from config.json
        # TODO: add multi type support
        self.playMusic(str(number) + '.wav')

    def playMusic(self, song):
        if self.__playingMusic:
            self.__playingMusic.stop()

        self.__playingMusic = Sound('music/' + song)
        self.__playingMusic.play()


if __name__ == "__main__":
    t65 = T65()
    t65.run() 