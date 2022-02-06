from tkinter import *
from pressuresensor import *
from time import *
import threading

class GuiUpdater (threading.Thread):

   def __init__ (self, threadID, name, diffPressActual, tempActual, pressureSensor):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.diffPressActual = diffPressActual
        self.tempActual = tempActual
        self.pressureSensor = pressureSensor

   def run (self):
        while True:
            self.diffPressActual = PressureSensor.readPressure()
            sleep(1)



class GUI:

    CONSTANTS = 0

    def __init__ (self, pressureSensor):
        self.pressureSensor = pressureSensor
        window = Tk ()
        window.title ("Sensorify (+config version)")
        self.diffPressActual = 0
        self.tempActual = 0
        Label (window, text="Differntial pressure (actual, Pa): ").grid (row = 0)
        Label (window, text="Temperature (actual, dgrC): ").grid (row = 1)
        Label (window, text=self.diffPressActual).grid (row=0, column=1)
        Label (window, text=self.tempActual).grid (row=1, column=1)
        window.mainloop ()
        thread1 = GuiUpdater (1, "updateThread", self.diffPressActual, self.tempActual, self.pressureSensor)
        thread1.start()