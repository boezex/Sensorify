from config import * 
from gui import *
from fan import *
from pressuresensor import *
import time
from threading import *
import csv


class MeasurementController:

    def __init__(self, fan, pressuresensor, conf) -> None:
        self.fan = fan
        self.pressuresensor = pressuresensor
        self.interface = None
        self.conf = conf
        self.workThread = Thread (target=self.measure)
        self.targetPressure = 0
        self.stopFlag = False

    def setGUI (self, interface) -> None:
        self.interface = interface
        
    def getIncreaseStep (self, currentPressure, isNulmeting) -> int:
        if isNulmeting:
            if (self.targetPressure > currentPressure):
                if (self.targetPressure - currentPressure) > 10:
                    return 300
                elif (self.targetPressure - currentPressure) > 5:
                    return 200
                elif (self.targetPressure - currentPressure) > 3:
                    return 150
                else:
                    return 100
        else:
            if (self.targetPressure > currentPressure):
                if (self.targetPressure - currentPressure) > 10:
                    return 1500
                elif (self.targetPressure - currentPressure) > 5:
                    return 750
                elif (self.targetPressure - currentPressure) > 3:
                    return 500
                else:
                    return 150

    def setFanFromPressure (self, isNulmeting, isBackwardMeasurement):
        currentPressure = self.pressuresensor.readPressure()
        currentFanSpeed = self.fan.getSetValue()
        if (self.targetPressure > currentPressure):
            while (self.targetPressure > currentPressure):
                if (self.stopFlag):
                    return
                self.fan.setSpeedRaw (currentFanSpeed + self.getIncreaseStep(currentPressure, isNulmeting))
                time.sleep (45)
                averagePressures = []
                for i in range (10):
                    averagePressures.append (self.pressuresensor.readPressure())
                    time.sleep (0.5)
                averagePressure = sum (averagePressures) / len (averagePressures)
                currentPressure = averagePressure
                currentFanSpeed = self.fan.getSetValue()
            return
        if (self.targetPressure < currentPressure and isBackwardMeasurement):
            while (self.targetPressure < currentPressure):
                if (self.stopFlag):
                    return
                targetSpeed = currentFanSpeed - self.getIncreaseStep(currentPressure, isNulmeting)
                if (targetSpeed > 0):   
                    self.fan.setSpeedRaw (targetSpeed)
                else:
                    self.fan.setSpeedRaw (0)
                time.sleep (45)
                averagePressures = []
                for i in range (10):
                    averagePressures.append (self.pressuresensor.readPressure())
                    time.sleep (0.5)
                averagePressure = sum (averagePressures) / len (averagePressures)
                currentPressure = averagePressure
                currentFanSpeed = self.fan.getSetValue()
            return


    def measure (self):
        mode, measurementTime, maxPressure, pressureInterval, isNulmeting, isBackwardMeasurement = self.conf.getMeasurementSettings ()
        self.interface.setCurrentStageAndPressure ("starting", pressureInterval)

        filename = "/home/pi/Desktop/metingen/"
        if isNulmeting:
            filename += "Nul-meting:"
        else:
            filename += "Meting:"
        description = self.conf.getDescriptionSettings().replace(" ", "")
        filename += description
        filename += ".csv"

        with open(filename, 'w', newline='') as file:
            writer = csv.writer (file)
            writer.writerow(["Pa", "l/s"])

            pressures = 0
            if mode == 1:
                pressures = [4, 8, 10, 15, 20, 30, 40, 60, 80, 100]
            if mode == 2:
                pressures = range(pressureInterval, maxPressure + pressureInterval, pressureInterval)
            if mode == 1 and isBackwardMeasurement:
                pressures = [100, 80, 60, 40, 30, 20, 15, 10, 8, 4]
            if mode == 2 and isBackwardMeasurement:
                pressures = range(maxPressure, 0, -pressureInterval)

            for pressure in pressures:
                if (self.stopFlag):
                    self.stopFlag = False
                    self.fan.setSpeedRaw (0)
                    self.interface.stopMeasurement (None)
                    return
                self.targetPressure = pressure
                self.interface.setCurrentStageAndPressure ("setting correct fan speed", self.targetPressure)
                self.setFanFromPressure (isNulmeting, isBackwardMeasurement)
                if (self.stopFlag):
                    self.stopFlag = False
                    self.fan.setSpeedRaw (0)
                    self.interface.stopMeasurement (None)
                    return
                self.interface.setCurrentStageAndPressure ("measuring", self.targetPressure)
                averagePressures = []
                averageAirflows = []
                for i in range (measurementTime * 2):
                    averagePressures.append (self.pressuresensor.readPressure())
                    averageAirflows.append (self.fan.getAirflowActual())
                    time.sleep (0.5)
                averagePressure = sum (averagePressures) / len (averagePressures)
                averageAirflow = sum (averageAirflows) / len (averageAirflows)
                averagePressure = round (averagePressure, 2)
                averageAirflow = round (averageAirflow, 2)
                self.interface.setPreviousPressureAirFlow (averagePressure, averageAirflow)
                writer.writerow([averagePressure, averageAirflow])
        self.fan.setSpeedRaw (0)
        self.interface.stopMeasurement (filename)

    def setFanFromPressureWrapper (self):
        self.interface.setCurrentStageAndPressure ("setting correct fan speed", self.targetPressure)
        self.setFanFromPressure (False)
        self.interface.stopSetFromPressure ()

    def startMeasurement (self):
        #if not self.workThread.is_alive:
        self.workThread = Thread (target=self.measure)
        self.workThread.start ()

    def startSetFromPressure (self, targetPressure):
        self.workThread = Thread (target=self.setFanFromPressureWrapper)
        self.targetPressure = targetPressure
        self.workThread.start ()

    def emergencyStop (self):
        self.fan.setSpeedRaw(0)
        self.stopFlag = True
