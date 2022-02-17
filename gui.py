from tkinter import *
from tkinter.messagebox import showerror
from tkinter.ttk import Separator

from pressuresensor import *
from config import *
from time import *
import threading

class GUI:

    CONSTANTS = 0

    def __init__ (self, pressureSensor, config, fan):
        self.pressureSensor = pressureSensor
        self.config = config
        self.mainFan = fan

        self.window = Tk ()
        self.window.title ("Sensorify (+config version)")
        self.window.geometry ("900x400")
        self.window.resizable (False,False)
        self.mode, self.measurementTime, self.maxPressure, self.pressureInterval = config.getMeasurementSettings ()
        self.radioButtons = IntVar ()
        self.radioButtons.set (self.mode)
        self.isBusy = False

        Label (self.window, text="Differential pressure (actual, Pa): ").grid (row = 0, padx=6, pady=6)
        Label (self.window, text="Temperature (actual, dgrC): ").grid (row = 1, padx=6, pady=6)
        Label (self.window, text="Fan Speed (actual, rpm / pct): ").grid (row = 2, padx=6, pady=6)
        Label (self.window, text="Fan Sensor value (actual, rpm): ").grid (row = 3, padx=6, pady=6)
        Label (self.window, text="Air Flow (actual, L/m): ").grid (row = 4, padx=6, pady=6)

        Button (self.window, text="Set pressure sensor 0.0", command=lambda: showerror ("Busy", "Can't set pressure sensor 0.0, currently busy!") if self.isBusy else self.pressureSensor.setZero()).grid (row = 6, columnspan=2, padx=6, pady=6)

        self.diffPressActualLabel = Label (self.window, text="0")
        self.diffPressActualLabel.grid (row=0, column=1, padx=6, pady=6)
        self.tempActualLabel = Label (self.window, text="0")
        self.tempActualLabel.grid (row=1, column=1, padx=6, pady=6)

        self.fanSpeedActualLabel = Label (self.window, text="0")
        self.fanSpeedActualLabel.grid (row=2, column=1, padx=6, pady=6)
        self.fanSensorActualLabel = Label (self.window, text="0")
        self.fanSensorActualLabel.grid (row=3, column=1, padx=6, pady=6)
        self.airFlowActualLabel = Label (self.window, text="0")
        self.airFlowActualLabel.grid (row=4, column=1, padx=6, pady=6)

        Separator (self.window, orient='vertical').grid (row=0, column=2, rowspan=6, sticky="ns", padx=6, pady=6)
        Separator (self.window, orient='horizontal').grid (row=7, column=0, columnspan=5, sticky="ew", padx=6, pady=6)


        Label (self.window, text= "Time to calculate average pressure difference(s):").grid (row=0, column=3, padx=6, pady=6)
        self.measurementTimeSlider = Scale (self.window, from_=10, to=240, orient='horizontal', resolution=10)
        self.measurementTimeSlider.set (self.measurementTime)
        self.measurementTimeSlider.grid (row=0, column=4, padx=6, pady=6)

        Label (self.window, text= "Measurement mode:").grid (row=1, column=3, padx=6, pady=6)
        self.nenRadioButton = Radiobutton (self.window, text="NEN-EN 13141-1 compliant", value=1, variable=self.radioButtons)
        self.customRadioButton = Radiobutton (self.window, text="Custom Pressure interval:", value=2, variable=self.radioButtons)
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

        Label (self.window, text= "Object description:").grid (row=5, column=3, padx=6, pady=6)
        self.descriptionEntry = Entry (self.window)
        self.descriptionEntry.grid (row=5, column=4, padx=6, pady=6)
        #self.descriptionEntry.set (self.description)

        Button (self.window, text="Start measurement!", command=lambda: self.startMeasurement() if pressureSensor.zeroIsSet else showerror ("0.0 not set", "Before starting a measurement, please set pressure sensor 0.0")).grid (row = 6, column=3, columnspan=2, padx=6, pady=6)
    
    def run (self):
        self.updateThread = Thread (target=self.updateGui, daemon=True)
        self.updateThread.start ()

        self.updateInstantThread = Thread (target=self.updateInstant, daemon=True)
        self.updateInstantThread.start ()

        self.window.mainloop ()

    def showError (self, title="Sensorify", message = "Error!"):
        showerror (title, message)

    def startMeasurement (self):
        self.isBusy = True
        self.measurementTime = self.measurementTimeSlider.get ()
        self.maxPressure = self.maxPressureSlider.get ()
        self.pressureInterval = self.pressureDiffSlider.get ()
        self.description = self.descriptionEntry.get ()
        self.config.setMeasurementSettings (self.mode, self.measurementTime, self.maxPressure, self.pressureInterval, self.description)
        self.mainFan.setSpeedRaw(int(self.descriptionEntry.get()))

    def updateInstant (self):
        while True:
            self.mode = self.radioButtons.get ()
            if self.mode == 1 or self.isBusy:
                self.maxPressureSlider.config(state=DISABLED,troughcolor = "grey")
                self.pressureDiffSlider.config(state=DISABLED,troughcolor = "grey")
            else:
                self.maxPressureSlider.config(state=NORMAL,takefocus=1,troughcolor = "#b3b3b3")
                self.pressureDiffSlider.config(state=NORMAL,takefocus=1,troughcolor = "#b3b3b3")

    def updateGui (self):
        while True:
            self.diffPressActualLabel["text"] = str(self.pressureSensor.readPressure())
            self.tempActualLabel["text"] = str(self.pressureSensor.readTemperature())
            self.fanSensorActualLabel["text"] = str(self.mainFan.getSensorSpeedActual())
            sleep(1)