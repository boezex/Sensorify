from threading import Thread, Lock
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
        self.mutex = Lock()

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

            RD_Pressure = self.i2cbus.read_word_data (self.i2c_address, self.BUFFER_0)
            actualPressure = (RD_Pressure - 1024) / 60000 * 150 - 150 / 2
        finally:
            self.mutex.release()
            return actualPressure

