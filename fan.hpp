#ifndef FAN_HPP
#define FAN_HPP
#include <modbus.h>

class Fan
{
    private:
    modbus_t *connection;

    public:
        Fan () {};
        ~Fan () {};
        void setSpeed (short percentage);
        void setSpeed (uint16_t raw);
        uint16_t readRegister (uint16_t address);

};


#endif