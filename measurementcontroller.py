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

    def setGUI (self, interface) -> None:
        self.interface = interface
        
    def getIncreaseStep (self, currentPressure = 0, isNulmeting = False):
        if isNulmeting:
            if (self.targetPressure > currentPressure):
                if (self.targetPressure - currentPressure) > 5:
                    return 800
                elif (self.targetPressure - currentPressure) > 3:
                    return 400
                else:
                    return 100
        else:
            if (self.targetPressure > currentPressure):
                if (self.targetPressure - currentPressure) > 5:
                    return 800
                elif (self.targetPressure - currentPressure) > 3:
                    return 400
                else:
                    return 100

    def setFanFromPressure (self):
        currentPressure = self.pressuresensor.readPressure()
        currentFanSpeed = self.fan.getSetValue()
        if (self.targetPressure > currentPressure):
            while (self.targetPressure > currentPressure):
                print
                self.fan.setSpeedRaw (currentFanSpeed + self.getIncreaseStep(currentPressure))
                time.sleep (30)
                averagePressures = []
                for i in range (25):
                    averagePressures.append (self.pressuresensor.readPressure())
                    time.sleep (0.2)
                averagePressure = sum (averagePressures) / len (averagePressures)
                currentPressure = averagePressure
                currentFanSpeed = self.fan.getSetValue()
        if (self.targetPressure < currentPressure):
            while (self.targetPressure < currentPressure):
                self.fan.setSpeedRaw (currentFanSpeed - 500)
                time.sleep (30)
                currentPressure = self.pressuresensor.readPressure()
                currentFanSpeed = self.fan.getSetValue()


    def measure (self):
        mode, measurementTime, maxPressure, pressureInterval = self.conf.getMeasurementSettings ()
        with open('meting1.csv', 'w', newline='') as file:

            if mode == 2:
                for pressure in range(pressureInterval, maxPressure, pressureInterval):
                    self.targetPressure = pressure
                    self.setFanFromPressure ()
                    averagePressures = []
                    averageAirflows = []
                    for i in range (measurementTime * 2):
                        averagePressures.append (self.pressuresensor.readPressure())
                        sensorSpeed = self.fan.getSensorSpeedActual ()
                        airflow = sensorSpeed * 472 / 40200
                        airflow /= 3.6
                        averageAirflows.append (airflow)
                        time.sleep (0.5)
                    averagePressure = sum (averagePressures) / len (averagePressures)
                    averageAirflow = sum (averageAirflows) / len (averageAirflows)
                    print (averagePressure)
                    print (averageAirflow)
                    writer = csv.writer (file)
                    writer.writerow([averagePressure, averageAirflow])


    def startMeasurement (self):
        if not self.measureThread.is_alive:
            self.measureThread.start ()
