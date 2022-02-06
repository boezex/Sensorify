from tkinter import *
from turtle import update
from pressuresensor import *
from time import *
import threading


def updateGui (diffPressActual, tempActual, pressureSensor):
    while True:
        diffPressActual = pressureSensor.readPressure()
        sleep(1)



class GUI:

    CONSTANTS = 0

    def __init__ (self, pressureSensor):
        self.pressureSensor = pressureSensor
        window = Tk ()
        window.title ("Sensorify (+config version)")
        self.diffPressActual = 0
        self.tempActual = 0
        Label (window, text="Differential pressure (actual, Pa): ").grid (row = 0)
        Label (window, text="Temperature (actual, dgrC): ").grid (row = 1)
        Label (window, text=self.diffPressActual).grid (row=0, column=1)
        Label (window, text=self.tempActual).grid (row=1, column=1)
        thread1 = Thread (target=updateGui, args= (self.diffPressActual, self.tempActual, self.pressureSensor), daemon=True)
        thread1.start ()
        window.mainloop ()