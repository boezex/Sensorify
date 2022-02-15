#include "fan.hpp"

Fan::Fan ()
{
    connection = modbus_new_rtu("/dev/ttyAMA0", 19200, 'E', 8, 1);
    modbus_set_slave(connection, 1);
    modbus_rtu_set_serial_mode(connection, MODBUS_RTU_RS485);
    modbus_rtu_set_rts(connection, MODBUS_RTU_RTS_DOWN);

    if (modbus_connect(connection) == -1) 
    {
        fprintf(stderr, "Connexion failed: %s\n", modbus_strerror(errno));
        modbus_free(connection);
        return -1;
    }

}

Fan::~Fan ()
{
    modbus_close(connection);
    modbus_free(connection);
}

void setSpeed (short percentage)
{
    if (percentage > 100)
    {
        return;
    }
    uint16_t rawSpeed = percentage * 65536; //65536 is max value
    modbus_write_register (connection, 53249, rawSpeed);
}

void setSpeed (uint16_t raw)
{
    modbus_write_register (connection, 53249, raw);
}

uint16_t readRegister (uint16_t register)
{
    uint16_t result[1];
    modbus_read_input_registers(connection, register, 1, result);
    return result[0];
}