from pydub import AudioSegment
from pydub.playback import play
import gpiozero
from signal import pause
import simpleaudio as sa
import time
import threading

import faulthandler
faulthandler.enable()

class T65:
    unhooked = False
    playingMusic = None

    def run(self):
        self.rotator = Rotator()
        self.rotator.when_dailed = self.dailed

        self.hook = gpiozero.Button(16) # TODO: replace with config
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

            if self.playingMusic or self.rotator.isDailing:
                time.sleep(.5)
                continue

            play = dailTone.play()
            play.wait_done()

    def offHook(self):
        print('off hook')
        self.unhooked = True

    def dailed(self, number):
        self.playMusic(str(number) + '.wav')

    def playMusic(self, song):
        if self.playingMusic:
            self.playingMusic.stop()
            del self.playingMusic

        music = sa.WaveObject.from_wave_file('music/' + song)
        self.playingMusic = music.play()
        self.playingMusic.wait_done()
        del self.playingMusic

class Rotator:
    isDailing = False
    count = -1 # starts at -1 because steps is trigged twice at the start
    lastNumber = -1
    __when_dailed = ...

    def __init__(self):
        self.step = gpiozero.Button(19) # TODO: replace with config
        self.step.when_pressed = self.step_pressed

        self.ison = gpiozero.Button(26) # TODO: replace with config
        self.ison.when_pressed = self.ison_pressed
        self.ison.when_released = self.ison_released
    
    def step_pressed(self):
        self.count += 1

    def ison_pressed(self):
        self.isDailing = True

    def ison_released(self):
        if self.count <= 0:
            self.count = -1
            return

        self.isDailing = False
        self.lastNumber = self.count
        self.count = -1 # reset counter
        self.dailed(self.lastNumber)

    @property
    def when_dailed(self):
        return self.__when_dailed

    @when_dailed.setter
    def when_dailed(self, value):
        self.__when_dailed = value

    def dailed(self, number):
        print('dailed ' + str(number))
        if self.when_dailed:
            self.when_dailed(number)


if __name__ == "__main__": 
    t65 = T65()
    t65.run() 