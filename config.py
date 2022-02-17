import configparser
from threading import Thread, Lock

class Config:

    def __init__(self):
        self.config = configparser.ConfigParser ()
        self.mutex = Lock ()
        self.config.read ("sensorify.config")
        if "measurement" not in self.config.sections ():
            self.setDefaults ()

    def writeConfig (self):
        self.mutex.acquire ()
        try:
            with open('sensorify.config', 'w') as configfile:
                self.config.write(configfile)
        finally:
            self.mutex.release ()

    def setDefaults (self):

            self.config['measurement'] = {}
            self.config['measurement']['mode'] = '1'
            self.config['measurement']['measurementTime'] = '60'
            self.config['measurement']['maxPressure'] = '150'
            self.config['measurement']['pressureInterval'] = '10'
            self.config['measurement']['description'] = '1'
        
            self.writeConfig ()

    def getMeasurementSettings (self):
        return int(self.config['measurement']['mode']), int(self.config['measurement']['measurementTime']), int(self.config['measurement']['maxPressure']), int(self.config['measurement']['pressureInterval'], int(self.config['measurement']['description']))

    def setMeasurementSettings (self, mode, measurementTime, maxPressure, pressureInterval, description):
        self.config['measurement'] = {}
        self.config['measurement']['mode'] = str(mode)
        self.config['measurement']['measurementTime'] = str(measurementTime)
        self.config['measurement']['maxPressure'] = str(maxPressure)
        self.config['measurement']['pressureInterval'] = str(pressureInterval)
        self.config['measurement']['description'] = description
    
        self.writeConfig ()