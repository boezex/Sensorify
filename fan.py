import serial
import serial.rs485

import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu

PORT = 1
#PORT = '/dev/ttyp5'

def main():
    """main"""
    logger = modbus_tk.utils.create_logger("console")

    try:
        #Connect to the slave
        ser = serial.rs485.RS485('/dev/ttyAMA0', 19200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_EVEN, stopbits=serial.STOPBITS_ONE, timeout=3, rtscts = True)
        ser.rs485_mode = serial.rs485.RS485Settings(rts_level_for_tx=False,
                                            rts_level_for_rx=True,
                                            delay_before_tx=0.0,
                                            delay_before_rx=-0.0)
        master = modbus_rtu.RtuMaster(ser)
        master.set_timeout(5.0)
        master.set_verbose(True)
        logger.info("connected")

        logger.info(master.execute(1, cst.READ_HOLDING_REGISTERS, 53505, 53506))
        logger.info(master.execute(1, cst.WRITE_SINGLE_REGISTER, 53249, output_value=30000))

        #send some queries
        #logger.info(master.execute(1, cst.READ_COILS, 0, 10))
        #logger.info(master.execute(1, cst.READ_DISCRETE_INPUTS, 0, 8))
        #logger.info(master.execute(1, cst.READ_INPUT_REGISTERS, 100, 3))
        #logger.info(master.execute(1, cst.READ_HOLDING_REGISTERS, 100, 12))
        #logger.info(master.execute(1, cst.WRITE_SINGLE_COIL, 7, output_value=1))
        #logger.info(master.execute(1, cst.WRITE_SINGLE_REGISTER, 100, output_value=54))
        #logger.info(master.execute(1, cst.WRITE_MULTIPLE_COILS, 0, output_value=[1, 1, 0, 1, 1, 0, 1, 1]))
        #logger.info(master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, 100, output_value=xrange(12)))

    except modbus_tk.modbus.ModbusError as exc:
        logger.error("%s- Code=%d", exc, exc.get_exception_code())

if __name__ == "__main__":
    main()