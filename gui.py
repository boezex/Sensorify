from tkinter import *
from tkinter.ttk import Separator
from turtle import update

from pressuresensor import *
from config import *
from time import *
import threading

class GUI:

    CONSTANTS = 0

    def __init__ (self, pressureSensor, config):
        self.pressureSensor = pressureSensor
        self.config = config

        self.window = Tk ()
        self.window.title ("Sensorify (+config version)")
        self.window.geometry ("900x400")
        self.window.resizable (False,False)
        self.mode, self.measurementTime, self.maxPressure, self.pressureInterval = config.getMeasurementSettings ()
        self.isBusy = False

        Label (self.window, text="Differential pressure (actual, Pa): ").grid (row = 0, padx=6, pady=6)
        Label (self.window, text="Temperature (actual, dgrC): ").grid (row = 1, padx=6, pady=6)

        Button (self.window, text="Set pressure sensor 0.0", command=lambda: self.pressureSensor.setZero()).grid (row = 3, columnspan=2, padx=6, pady=6)

        self.diffPressActualLabel = Label (self.window, text="0")
        self.diffPressActualLabel.grid (row=0, column=1, padx=6, pady=6)
        self.tempActualLabel = Label (self.window, text="0")
        self.tempActualLabel.grid (row=1, column=1, padx=6, pady=6)

        Separator (self.window, orient='vertical').grid (row=1, column=2, rowspan=4, sticky="ns")
        Separator (self.window, orient='horizontal').grid (row=6, column=1, rowspan=4, sticky="ew", padx=6, pady=6)


        Label (self.window, text= "Time to calculate average pressure difference(s):").grid (row=0, column=3, padx=6, pady=6)
        self.measurementTimeSlider = Scale (self.window, from_=10, to=240, orient='horizontal', resolution=10)
        self.measurementTimeSlider.set (self.measurementTime)
        self.measurementTimeSlider.grid (row=0, column=4, padx=6, pady=6)

        Label (self.window, text= "Measurement mode:").grid (row=1, column=3, padx=6, pady=6)
        self.nenRadioButton = Radiobutton (self.window, text="NEN-EN 13141-1 compliant", value=1, variable=self.mode)
        self.customRadioButton = Radiobutton (self.window, text="Custom Pressure interval:", value=2, variable=self.mode)
        self.nenRadioButton.grid (row=1, column=4, padx=6, pady=6)
        self.customRadioButton.grid (row=2, column=4, padx=6, pady=6)

        Label (self.window, text= "Max Pressure to test (Pa)").grid (row=3, column=3, padx=6, pady=6)
        Label (self.window, text= "Difference in pressure between measurements (Pa)").grid (row=4, column=3, padx=6, pady=6)
        self.maxPressureSlider = Scale (self.window, from_=10, to=250, orient='horizontal', resolution=10)
        self.maxPressureSlider.set (self.maxPressure)
        self.maxPressureSlider.grid (row=3, column=4, padx=6, pady=6)

        self.pressureDiffSlider = Scale (self.window, from_=2, to=15, orient='horizontal')
        self.pressureDiffSlider.set (self.pressureInterval)
        self.pressureDiffSlider.grid (row=4, column=4, padx=6, pady=6)



        Button (self.window, text="Start measurement!", command=self.startMeasurement()).grid (row = 5, column=3, columnspan=2, padx=6, pady=6)

        self.updateThread = Thread (target=self.updateGui, daemon=True)
        self.updateThread.start ()

        self.updateInstantThread = Thread (target=self.updateInstant, daemon=True)
        self.updateInstantThread.start ()

        self.window.mainloop ()

    def startMeasurement (self):
        self.isBusy = True

    def updateInstant (self):
        while True:
            if self.mode == 1 or self.isBusy:
                self.maxPressureSlider.config(state=DISABLED,takefocus=0)
                self.pressureDiffSlider.config(state=DISABLED,takefocus=0)
            else:
                self.maxPressureSlider.config(state=NORMAL,takefocus=1)
                self.pressureDiffSlider.config(state=NORMAL,takefocus=1)

    def updateGui (self):
        while True:
            self.diffPressActualLabel["text"] = str(self.pressureSensor.readPressure())
            self.tempActualLabel["text"] = str(self.pressureSensor.readTemperature())
            sleep(1)