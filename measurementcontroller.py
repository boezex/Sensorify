from gui import *
from fan import *
from pressuresensor import *
import time


class MeasurementController:

    def __init__(self, fan, pressuresensor) -> None:
        self.fan = fan
        self.pressuresensor = pressuresensor
        self.interface = None

    def setGUI (self, interface) -> None:
        self.interface = interface

    def setFanFromPressure (self, targetPressure):
        currentPressure = self.pressuresensor.readPressure()
        currentFanSpeed = self.fan.getSetValue()
        if (targetPressure > currentPressure):
            while (targetPressure > currentPressure):
                self.fan.setSpeedRaw (currentFanSpeed + 100)
                time.sleep (10)
                currentPressure = self.pressuresensor.readPressure()
                currentFanSpeed = self.fan.getSetValue()


            

    def startMeasurement (self, description):
        self.setFanFromPressure (int(description))