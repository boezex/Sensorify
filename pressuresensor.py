from threading import Thread, Lock
from typing import final
from smbus import SMBus
import time

class PressureSensor:

    D6FPH_ADDRESS = 0x6C
    SENS_CTRL = 0xD040
    COMP_DATA1_H = 0xD051
    TMP_H = 0xD061
    BUFFER_0 = 0x07
    CTRL_REG = 0x0B
    START_ADDRESS = 0x00

    def __init__ (self, i2c_address = D6FPH_ADDRESS):
        self.i2c_address = i2c_address
        self.i2cbus = SMBus (1)
        # misschien nog resetten?
        self.i2cbus.write_byte_data (self.i2c_address, self.CTRL_REG, 0x00)
        time.sleep(0.1)
        self.zeroIsSet = False
        self.compensation = 0.0
        self.mutex = Lock()

    def setZero (self):
        self.compensation = self.readPressureRaw ()
        self.zeroIsSet = True
    
    def isSetZero (self):
        return self.zeroIsSet
        
    def toBigEndian(self, data):
        tmpData = data.to_bytes (2, 'big')
        return int.from_bytes(tmpData, 'little')

    def enterMCUMode (self):
        data = [0xD0, 0x40, 0x18, 0x06]
        self.i2cbus.write_i2c_block_data (self.i2c_address, self.START_ADDRESS, data)
        time.sleep(0.033)

    def readPressure (self):
        self.mutex.acquire()
        try:
            self.enterMCUMode()

            data = [0xD0, 0x51, 0x2C]
            self.i2cbus.write_i2c_block_data (self.i2c_address, self.START_ADDRESS, data)

            Rv = self.i2cbus.read_word_data (self.i2c_address, self.BUFFER_0)
            RvBigEndian = self.toBigEndian (Rv)

            actualPressure = (RvBigEndian - 1024) / 60000 * 250
            actualPressure -= self.compensation
        finally:
            self.mutex.release()
            return round (actualPressure, 2)

    def readPressureRaw (self):
        self.mutex.acquire()
        try:
            self.enterMCUMode()

            data = [0xD0, 0x51, 0x2C]
            self.i2cbus.write_i2c_block_data (self.i2c_address, self.START_ADDRESS, data)

            Rv = self.i2cbus.read_word_data (self.i2c_address, self.BUFFER_0)
            RvBigEndian = self.toBigEndian (Rv)

            actualPressure = (RvBigEndian - 1024) / 60000 * 250
        finally:
            self.mutex.release()
            return actualPressure

    def readTemperature (self):
        self.mutex.acquire()
        try:
            self.enterMCUMode()

            data = [0xD0, 0x61, 0x2C]
            self.i2cbus.write_i2c_block_data (self.i2c_address, self.START_ADDRESS, data)

            Rv = self.i2cbus.read_word_data (self.i2c_address, self.BUFFER_0)
            RvBigEndian = self.toBigEndian (Rv)
            
            actualTemperature = (RvBigEndian - 10214) / 37.39
        finally:
            self.mutex.release()
            return round (actualTemperature, 2)


