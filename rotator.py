import gpiozero

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