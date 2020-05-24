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

    def __init__(self, file):
        self.file = file

    def play(self):
        self.__playing = True
        self.__thread = threading.Thread(target=self._play)
        self.__thread.start()
    
    def stop(self):
        self.__playing = False

    def isPlaying(self):
        return self.__playing

    def pause(self):
        self.__pause = False

    def unpause(self):
        self.__pause = True

    def _play(self):
        self.__playing = True
        wf = wave.open(self.file, 'rb')

        p = pyaudio.PyAudio()

        # open stream
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        # read frame
        data = wf.readframes(Sound.CHUNK)

        # play stream
        while self.__playing:
            if len(data) == 0:
                # when end of sound
                if self.repeat:
                    wf.rewind()
                else:
                    break
            
            if not self.__pause:
                time.sleep(.5)
                continue

            stream.write(data)
            # read next frame
            data = wf.readframes(Sound.CHUNK)

        # stop stream (4)
        stream.stop_stream()
        stream.close()

        # close PyAudio (5)
        p.terminate()
    
    def wait_done(self):
        self.__thread.join()