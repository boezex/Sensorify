CXX = g++
CXXFLAGS = -std=c++11 -I /usr/include/modbus -lmodbus -lpthread

main: readregister readinputregister writeregister
	@echo appaatjes worden gebouwd
	chmod +x readRegister readInputRegister writeRegister


readregister: readRegister.cpp
	$(CXX) $(CXXFLAGS) -o readRegister readRegister.cpp

readinputregister: readInputRegister.cpp
	$(CXX) $(CXXFLAGS) -o readInputRegister readInputRegister.cpp

writeregister: writeRegister.cpp
	$(CXX) $(CXXFLAGS) -o writeRegister writeRegister.cpp

.PHONY: clean
clean:
	rm -r readRegister readInputRegister writeRegister