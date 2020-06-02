import pyaudio
import wave
import threading
import time

class Sound:
    CHUNK = 1024
    
    # thread playing sound
    __thread = None
    __pause = False
    __playing = False
    repeat = False

    def __init__(self, player, file):
        self.player = player
        self.file = file

    def play(self):
        if self.__thread and self.__thread.isAlive():
            self.__thread.join() # first finish previous thread before starting a new one

        self.__thread = threading.Thread(target=self.__play)
        self.__thread.start()
    
    def stop(self):
        self.__playing = False

    def isPlaying(self):
        return self.__playing

    def pause(self):
        self.__pause = True

    def unpause(self):
        self.__pause = False

    def isPaused(self):
        return self.__pause

    def __play(self):
        self.__playing = True
        # TODO: add multi type support
        wf = wave.open(self.file, 'rb')

        # open stream
        stream = self.player.open(format=self.player.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        # read frame
        data = wf.readframes(Sound.CHUNK)

        try:
            # play stream
            while self.__playing:
                if len(data) == 0:
                    # when end of sound
                    if self.repeat:
                        wf.rewind()
                    else:
                        break
                
                if self.__pause:
                    time.sleep(.5)
                    continue

                stream.write(data)
                # read next frame
                data = wf.readframes(Sound.CHUNK)
        finally:
            # stop stream
            stream.stop_stream()
            stream.close()
            self.__playing = False
    
    def wait_done(self):
        self.__thread.join()