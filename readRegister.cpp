#include <stdio.h>
#ifndef _MSC_VER
#include <unistd.h>
#endif
#include <stdlib.h>
#include <errno.h>

#include <iostream>
#include <complex> 
#include <modbus.h>

int main (int argc, char *argv[])
{

    modbus_t *connection = modbus_new_rtu("/dev/ttyAMA0", 19200, 'E', 8, 1);
    modbus_set_slave(connection, 1);
    modbus_rtu_set_serial_mode(connection, MODBUS_RTU_RS485);
    modbus_rtu_set_rts(connection, MODBUS_RTU_RTS_DOWN);

    if (modbus_connect(connection) == -1) 
    {
        fprintf(stderr, "Connexion failed: %s\n", modbus_strerror(errno));
        modbus_free(connection);
        return -1;
    }

    if (argc != 2)
    {
        std::cerr << "Only pass 1 argument!" << std::endl;
        modbus_close(connection);
        modbus_free(connection);
        return -1;
    }

    uint16_t result[1];
    modbus_read_registers(connection, (int) argv[1], 1, result);


    std::cout << result[0] << std::endl;

    modbus_close(connection);
    modbus_free(connection);

    return 0;

}