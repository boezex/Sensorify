#include <fan.hpp>
#include <iostream>

Fan fan ();

short pct = 30;
fan.setSpeed(pct);

std::cout << "fan speed current: " << fan.readRegister (53264) << std::endl;