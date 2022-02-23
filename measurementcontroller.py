from audioop import avg
from gui import *
from fan import *
from pressuresensor import *
import time
from threading import *


class MeasurementController:

    def __init__(self, fan, pressuresensor) -> None:
        self.fan = fan
        self.pressuresensor = pressuresensor
        self.interface = None
        self.setFanThread = Thread (target=self.setFanFromPressure, args=[int(description)])

    def setGUI (self, interface) -> None:
        self.interface = interface

    def setFanFromPressure (self, targetPressure):
        currentPressure = self.pressuresensor.readPressure()
        currentFanSpeed = self.fan.getSetValue()
        if (targetPressure > currentPressure):
            while (targetPressure > currentPressure):
                self.fan.setSpeedRaw (currentFanSpeed + 100)
                time.sleep (10)
                averagePressures = []
                for i in range (50):
                    averagePressures.append (self.pressuresensor.readPressure())
                    time.sleep (0.1)
                averagePressure = sum (averagePressures) / len (averagePressures)
                print (averagePressures)
                print (averagePressure)
                currentPressure = averagePressure
                currentFanSpeed = self.fan.getSetValue()
        if (targetPressure < currentPressure):
            while (targetPressure < currentPressure):
                self.fan.setSpeedRaw (currentFanSpeed - 100)
                time.sleep (10)
                currentPressure = self.pressuresensor.readPressure()
                currentFanSpeed = self.fan.getSetValue()


            

    def startMeasurement (self, description):
        self.setFanThread.start ()