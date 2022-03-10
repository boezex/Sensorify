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
        self.measureThread = Thread (target=self.measure)
        self.targetPressure = 0
        self.stopFlag = False

    def setGUI (self, interface) -> None:
        self.interface = interface
        
    def getIncreaseStep (self, currentPressure, isNulmeting):
        if isNulmeting:
            if (self.targetPressure > currentPressure):
                if (self.targetPressure - currentPressure) > 5:
                    return 600
                elif (self.targetPressure - currentPressure) > 3:
                    return 300
                else:
                    return 150
        else:
            if (self.targetPressure > currentPressure):
                if (self.targetPressure - currentPressure) > 5:
                    return 1000
                elif (self.targetPressure - currentPressure) > 3:
                    return 400
                else:
                    return 200

    def setFanFromPressure (self, isNulmeting):
        currentPressure = self.pressuresensor.readPressure()
        currentFanSpeed = self.fan.getSetValue()
        if (self.targetPressure > currentPressure):
            while (self.targetPressure > currentPressure):
                if (self.stopFlag):
                    return
                self.fan.setSpeedRaw (currentFanSpeed + self.getIncreaseStep(currentPressure, isNulmeting))
                time.sleep (30)
                averagePressures = []
                for i in range (10):
                    averagePressures.append (self.pressuresensor.readPressure())
                    time.sleep (0.5)
                averagePressure = sum (averagePressures) / len (averagePressures)
                currentPressure = averagePressure
                currentFanSpeed = self.fan.getSetValue()
            return
        if (self.targetPressure < currentPressure):
            while (self.targetPressure < currentPressure):
                self.fan.setSpeedRaw (currentFanSpeed - 500)
                time.sleep (30)
                currentPressure = self.pressuresensor.readPressure()
                currentFanSpeed = self.fan.getSetValue()
            return


    def measure (self):
        mode, measurementTime, maxPressure, pressureInterval, isNulmeting = self.conf.getMeasurementSettings ()
        self.interface.setCurrentStageAndPressure ("starting", pressureInterval)
        filename = "Meting xxx.csv"
        with open(filename, 'w', newline='') as file:
            writer = csv.writer (file)

            if mode == 2:
                for pressure in range(pressureInterval, maxPressure + pressureInterval, pressureInterval):
                    if (self.stopFlag):
                        self.stopFlag = False
                        self.fan.setSpeedRaw (0)
                        self.interface.stopMeasurement ()
                        return
                    self.targetPressure = pressure
                    self.interface.setCurrentStageAndPressure ("setting correct fan speed", self.targetPressure)
                    self.setFanFromPressure (isNulmeting)
                    if (self.stopFlag):
                        self.stopFlag = False
                        self.fan.setSpeedRaw (0)
                        self.interface.stopMeasurement ()
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
                    self.interface.setPreviousPressureAirFlow (averagePressure, averageAirflow)
                    writer.writerow([averagePressure, averageAirflow])
        self.fan.setSpeedRaw (0)
        self.interface.stopMeasurement (filename)


    def startMeasurement (self):
        #if not self.measureThread.is_alive:
        self.measureThread.start ()

    def emergencyStop (self):
        self.stopFlag = True
