from pydub import AudioSegment
from pydub.playback import play
import gpiozero
from signal import pause
#import time

class T65:
    count = -1 # starts at -1 because steps is trigged twice at the start
    triggered = False

    def run(self):        
        step = gpiozero.Button(19)
        step.when_pressed = self.step_pressed

        ison = gpiozero.Button(26)
        ison.when_pressed = self.ison_pressed

        # kiestoon = AudioSegment.from_ogg("kiestoon.ogg")
        # play(kiestoon)

        #while True:
        #    print(count)
        #    time.sleep(1)
        pause()

    def step_pressed(self):
        self.count += 1
        print("step pressed! " + str(self.count))

    def ison_pressed(self):
        print("ison pressed!")
        if False:
            sound = AudioSegment.from_file("1.wav", format="wav")
            play(sound)


def main():
    t65 = T65()
    t65.run()

if __name__ == "__main__":
    main()