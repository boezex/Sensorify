from threading import Thread, Lock
import subprocess
from gui import *

class Fan:

    def __init__(self):
        self.mutex = Lock ()
        self.interface = None

    def setGUI (self, interface) -> None:
        self.interface = interface

    def setSpeedRaw (self, speed) -> None:
        self.mutex.acquire ()
        try:
            result = subprocess.run (['./writeRegister', '53249', speed], capture_output=True)
            if result.returncode is -1:
                self.interface.showError("Modbus error", "ModbusError!")
        finally:
            self.mutex.release ()

    def getFanSpeedActual (self) -> int:
        self.mutex.acquire ()
        returnValue = 0
        try:
            result = subprocess.run (['./readInputRegister', '53264'], capture_output=True)
            if result.returncode is -1:
                self.interface.showError("Modbus error", "ModbusError!")
            else:
                returnValue = int(result.stdout)
        finally:
            self.mutex.release ()
            return returnValue
    
    def getSetValue (self) -> int:
        self.mutex.acquire ()
        returnValue = 0
        try:
            result = subprocess.run (['./readInputRegister', '53274'], capture_output=True)
            if result.returncode is -1:
                self.interface.showError("Modbus error", "ModbusError!")
            else:
                returnValue = int(result.stdout)
        finally:
            self.mutex.release ()
            return returnValue

    