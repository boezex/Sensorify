from threading import Thread, Lock
import subprocess
from gui import *

class Fan:

    def __init__ (self):
        self.mutex = Lock ()
        self.interface = None
        self.setValue = 0
    
    def __del__ (self):
        self.setSpeedRaw (0)

    def setGUI (self, interface) -> None:
        self.interface = interface

    def setSpeedPCT (self, pct) -> None:
        if (pct > 100):
            return
        pct /= 100
        speed = 65536 * pct

    def setSpeedRaw (self, speed) -> None:
        if (speed > 65536):
            return
        self.mutex.acquire ()
        self.setValue = speed
        try:
            result = subprocess.run (['./writeRegister', '53249', str(speed)], capture_output=True)
            if result.returncode == -1:
                self.interface.showError("Modbus error", "ModbusError!")
        finally:
            self.mutex.release ()

    def getFanSpeedActualPCT (self) -> int:
        speed = self.getFanSpeedActual ()
        speed /= 65536
        speed *= 100
        return speed

    def getFanSpeedActual (self) -> int:
        self.mutex.acquire ()
        returnValue = 0
        try:
            result = subprocess.run (['./readInputRegister', '53264'], capture_output=True)
            if result.returncode == -1:
                self.interface.showError("Modbus error", "ModbusError!")
            else:
                returnValue = int(result.stdout)
        finally:
            self.mutex.release ()
            return returnValue
        
    def getSensorSpeedActual (self) -> int:
        self.mutex.acquire ()
        returnValue = 0
        try:
            result = subprocess.run (['./readInputRegister', '53275'], capture_output=True)
            if result.returncode == -1:
                self.interface.showError("Modbus error", "ModbusError!")
            else:
                returnValue = int(result.stdout)
        finally:
            self.mutex.release ()
            return returnValue
    
    def getAirflowActual (self) -> int:
        self.mutex.acquire ()
        returnValue = 0
        try:
            result = subprocess.run (['./readInputRegister', '53299'], capture_output=True)
            if result.returncode == -1:
                self.interface.showError("Modbus error", "ModbusError!")
            else:
                returnValue = int(result.stdout)
                returnValue /= 3.6
        finally:
            self.mutex.release ()
            return returnValue

    
    def getSetValue (self) -> int:
        return self.setValue

    