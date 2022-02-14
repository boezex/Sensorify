import configparser
from threading import Thread, Lock

class Config:

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.mutex = Lock()
        self.config.read ("sensorify.config")

    def writeConfig (self):
        self.mutex.acquire ()
        try:
            with open('sensorify.config', 'w') as configfile:
                self.config.write(configfile)
        finally:
            self.mutex.release ()

    def setDefaults (self):
        
            self.config['measurement']['mode'] = 1
            self.config['measurement']['measurementTime'] = 60
            self.config['measurement']['maxPressure'] = 150
            self.config['measurement']['pressureInterval'] = 10
        
            self.writeConfig ()

    def getMeasurementSettings (self):
        return self.config['measurement']['mode'], self.config['measurement']['measurementTime'], self.config['measurement']['maxPressure'], self.config['measurement']['pressureInterval']

    def setMeasurementSettings (self, mode, measurementTime, maxPressure, pressureInterval):
        self.config['measurement']['mode'] = mode
        self.config['measurement']['measurementTime'] = measurementTime
        self.config['measurement']['maxPressure'] = maxPressure
        self.config['measurement']['pressureInterval'] = pressureInterval
    
        self.writeConfig ()