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

    def enterMCUMode (self):
        data = [0xD0, 0x40, 0x18, 0x06]
        self.i2cbus.write_block_data (self.i2c_address, self.START_ADDRESS, data)

    def readPressure (self):
        self.enterMCUMode()

        tmpData = [ 0xD0, 0x51, 0x2C, 0x07]
        RD_Pressure = self.i2cbus.block_process_call (self.i2c_address, self.START_ADDRESS, tmpData)
        print (RD_Pressure)


sens = PressureSensor

sens.readPressure()