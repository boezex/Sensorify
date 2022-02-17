from gui import *
from fan import *
from pressuresensor import *


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
            