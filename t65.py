#!/usr/bin/python3.7

import gpiozero
import time
import threading
import json
import subprocess
from rotator import Rotator
from sound import Sound
import pyaudio

class T65:
    HOOK_PIN_DEFAULT = 16
    DAILER_STEP_PIN_DEFAULT = 19
    DAILER_ISON_PIN_DEFAULT = 26

    config = {}
    musicConfig = {}

    __dailTone = None
    rotator = None
    hook = None
    __playingMusic = None
    unhooked = False

    def run(self):
        self.__loadConfigs()

        self.audio = pyaudio.PyAudio()
        # hacky solution, but in this way the console will only print the error once
        for ii in range(self.audio.get_device_count()):
            self.audio.get_device_info_by_index(ii)

        self.__dailTone = Sound(self.audio, './music/kiestoon-2s.wav')
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

        self.__mainLoop()

    def __loadConfigs(self):
        with open('config.json') as json_file:
            self.config = json.load(json_file)
        with open('music.json') as json_file:
            self.musicConfig = json.load(json_file)
        # load and set volume level
        with open('volume.json') as json_file:
            volume = json.load(json_file)
            subprocess.call(["python3", "./vol.py", volume.get('Volume')])

    def __mainLoop(self):
        while True:
            if self.__playingMusic and not self.__playingMusic.isPlaying():
                del self.__playingMusic
                if not self.__dailTone.isPlaying():
                    self.__dailTone.play()
            if self.rotator.isDailing and self.__dailTone.isPlaying():
                self.__dailTone.stop()

            time.sleep(1)

    def onHook(self):
        print('on hook')
        self.stopMusic()
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

        song = self.musicConfig[number]
        self.playMusic(song)

    def playMusic(self, song):
        if self.__playingMusic:
            self.__playingMusic.stop()

        self.__playingMusic = Sound(self.audio, 'music/' + song)
        self.__playingMusic.play()
    
    def stopMusic(self):
        if self.__playingMusic: # stop music if playing
            self.__playingMusic.stop()
            del self.__playingMusic

if __name__ == "__main__":
    t65 = T65()
    t65.run()