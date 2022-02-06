from tkinter import *
from turtle import update
from pressuresensor import *
from time import *
import threading


def updateGui (diffPressActual, tempActual, pressureSensor):
    while True:
        diffPressActual["text"] = str(pressureSensor.readPressure())
        sleep(1)



class GUI:

    CONSTANTS = 0

    def __init__ (self, pressureSensor):
        self.pressureSensor = pressureSensor
        window = Tk ()
        window.title ("Sensorify (+config version)")
        Label (window, text="Differential pressure (actual, Pa): ").grid (row = 0)
        Label (window, text="Temperature (actual, dgrC): ").grid (row = 1)
        self.diffPressActualLabel = Label (window, text="0").grid (row=0, column=1)
        self.tempActualLabel = Label (window, text="0").grid (row=1, column=1)
        thread1 = Thread (target=updateGui, args= (self.diffPressActualLabel, self.tempActualLabel, self.pressureSensor), daemon=True)
        thread1.start ()
        window.mainloop ()