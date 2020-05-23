from pydub import AudioSegment
from pydub.playback import play
import gpiozero
from signal import pause
import simpleaudio as sa
import time
import threading
import json
from rotator import Rotator

class T65:
    HOOK_PIN_DEFAULT = 16
    DAILER_STEP_PIN_DEFAULT = 19
    DAILER_ISON_PIN_DEFAULT = 26

    unhooked = False
    playingMusic = None

    def run(self):
        with open('config.json') as json_file:
            self.config = json.load(json_file)

        self.rotator = Rotator(
            self.config.get('DialerRedGpio', self.DAILER_STEP_PIN_DEFAULT),
            self.config.get('DialerYellowGpio', self.DAILER_ISON_PIN_DEFAULT)
        )
        self.rotator.when_dailed = self.dailed

        self.hook = gpiozero.Button(self.config.get('HookGpio', self.HOOK_PIN_DEFAULT))
        self.hook.when_released = self.offHook
        self.hook.when_pressed = self.onHook
        if not self.hook.is_pressed: # start offHook when it's already of the hook
            self.offHook()

        threading.Thread(name='dailer', target=self.playDailTone).start()
        print('t65 started')
        pause()

    def onHook(self):
        print('on hook')
        self.unhooked = False

    def playDailTone(self):
        dailTone = sa.WaveObject.from_wave_file('music/kiestoon-2s.wav')

        while(True):
            if not self.unhooked:
                time.sleep(1)
                continue

            if self.playingMusic or self.rotator.isDailing:
                time.sleep(.5)
                continue

            play = dailTone.play()
            play.wait_done()

    def offHook(self):
        print('off hook')
        self.unhooked = True

    def dailed(self, number):
        # TODO: add multi type support
        self.playMusic(str(number) + '.wav')

    def playMusic(self, song):
        if self.playingMusic:
            self.playingMusic.stop()
            del self.playingMusic

        music = sa.WaveObject.from_wave_file('music/' + song)
        self.playingMusic = music.play()
        self.playingMusic.wait_done()
        del self.playingMusic


if __name__ == "__main__": 
    t65 = T65()
    t65.run() 