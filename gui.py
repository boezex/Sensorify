from tkinter import *
from turtle import update
from pressuresensor import *
from time import *
import threading

class GUI:

    CONSTANTS = 0

    def __init__ (self, pressureSensor):
        self.pressureSensor = pressureSensor

        self.window = Tk ()
        self.window.title ("Sensorify (+config version)")

        Label (self.window, text="Differential pressure (actual, Pa): ").grid (row = 0)
        Label (self.window, text="Temperature (actual, dgrC): ").grid (row = 1)

        self.diffPressActualLabel = Label (self.window, text="0")
        self.diffPressActualLabel.grid (row=0, column=1)
        self.tempActualLabel = Label (self.window, text="0")
        self.tempActualLabel.grid (row=1, column=1)

        self.updateThread = Thread (target=self.updateGui, daemon=True)
        self.updateThread.start ()
        self.window.mainloop ()

    def updateGui (self):
        while True:
            self.diffPressActualLabel["text"] = str(self.pressureSensor.readPressure())
            self.tempActualLabel["text"] = str(self.pressureSensor.readTemperature())
            sleep(1)