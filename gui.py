from tkinter import *
from tkinter.ttk import Separator
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
        self.window.geometry ("800x300")
        self.window.resizable (False,False)
        self.mode = 1

        Label (self.window, text="Differential pressure (actual, Pa): ").grid (row = 0, padx=6, pady=6)
        Label (self.window, text="Temperature (actual, dgrC): ").grid (row = 1, padx=6, pady=6)

        Button (self.window, text="Set pressure sensor 0.0", command=lambda: self.pressureSensor.setZero()).grid (row = 3, columnspan=2, padx=6, pady=6)

        self.diffPressActualLabel = Label (self.window, text="0")
        self.diffPressActualLabel.grid (row=0, column=1, padx=6, pady=6)
        self.tempActualLabel = Label (self.window, text="0")
        self.tempActualLabel.grid (row=1, column=1, padx=6, pady=6)

        self.separator = Separator (self.window, orient='vertical')
        self.separator.grid (row=0, column=2, rowspan=3, sticky="ns", padx=6, pady=6)

        Label (self.window, text= "Time to calculate average pressure diff(s):").grid (row=0, column=3, padx=6, pady=6)
        self.measurementTimeSlider = Scale (self.window, from_=10, to=240, orient='horizontal')
        self.measurementTimeSlider.grid (row=0, column=4, padx=6, pady=6)

        Label (self.window, text= "Measurement mode:").grid (row=1, column=3, padx=6, pady=6)
        self.nenRadioButton = Radiobutton (self.window, text="NEN-EN 13141-1 compliant", value=1, variable=self.mode)
        self.customRadioButton = Radiobutton (self.window, text="Custom Pressure interval:", value=2, variable=self.mode)
        self.nenRadioButton.grid (row=1, column=3, padx=6, pady=6)
        self.customRadioButton.grid (row=3, column=3, padx=6, pady=6)

        Label (self.window, text= "Max Pressure to test (Pa)").grid (row=4, column=3, padx=6, pady=6)
        Label (self.window, text= "Difference in pressure between measurements (Pa)").grid (row=5, column=3, padx=6, pady=6)
        self.maxPressureSlider = Scale (self.window, from_=10, to=250, orient='horizontal')
        self.maxPressureSlider.grid (row=4, column=4, padx=6, pady=6)

        self.PressureDiffSlider = Scale (self.window, from_=2, to=15, orient='horizontal')
        self.PressureDiffSlider.grid (row=5, column=4, padx=6, pady=6)



        Button (self.window, text="Start measurement!").grid (row = 6, column=3, columnspan=2, padx=6, pady=6)

        self.updateThread = Thread (target=self.updateGui, daemon=True)
        self.updateThread.start ()

        self.window.mainloop ()

    def updateGui (self):
        while True:
            self.diffPressActualLabel["text"] = str(self.pressureSensor.readPressure())
            self.tempActualLabel["text"] = str(self.pressureSensor.readTemperature())
            sleep(1)