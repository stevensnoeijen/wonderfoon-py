from pydub import AudioSegment
from pydub.playback import play
import gpiozero
from signal import pause
import simpleaudio as sa
import time

import faulthandler
faulthandler.enable()

class T65:
    unhooked = False
    playing = None

    def run(self):
        hook = gpiozero.Button(16) # TODO: replace with config
        hook.when_released = self.offHook
        hook.when_pressed = self.onHook

        self.rotator = Rotator()
        self.rotator.when_dailed = self.dailed

        print('t65 started')
        pause()

    def onHook(self):
        self.unhooked = False

    def playDailTone(self):
        dailTone = sa.WaveObject.from_wave_file('music/kiestoon-2s.wav')

        while(self.unhooked):
            play = dailTone.play()
            play.wait_done()
            play.stop()
            del play

    def offHook(self):
        self.unhooked = True
        self.playDailTone()

    def dailed(self, number):
        self.playMusic(str(number) + '.wav')

    def playMusic(self, song):
        if(self.playing):
            self.playing.stop()
            del self.playing

        audio = sa.WaveObject.from_wave_file('music/' + song)
        self.playing = audio.play()
        self.playing.wait_done()
        del self.playing

class Rotator:
    count = -1 # starts at -1 because steps is trigged twice at the start
    lastNumber = -1
    __when_dailed = ...

    def __init__(self):
        self.step = gpiozero.Button(19) # TODO: replace with config
        self.step.when_pressed = self.step_pressed

        self.ison = gpiozero.Button(26) # TODO: replace with config
        self.ison.when_released = self.ison_released
    
    def step_pressed(self):
        self.count += 1

    def ison_released(self):
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
        if(self.when_dailed):
            self.when_dailed(number)


if __name__ == "__main__": 
    t65 = T65()
    t65.run() 