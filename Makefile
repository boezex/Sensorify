CXX = g++
CXXFLAGS = -std=c++11 -I /usr/include/modbus -lmodbus -lpthread

main: readregister readinputregister writeregister
	@echo appaatjes worden gebouwd
	chmod +x readRegister readInputRegister writeRegister


readregister: readRegister.cpp
	$(CXX) readRegister.cpp $(CXXFLAGS) -o readRegister

readinputregister: readInputRegister.cpp
	$(CXX) readInputRegister.cpp $(CXXFLAGS) -o readInputRegister

writeregister: writeRegister.cpp
	$(CXX) writeRegister.cpp $(CXXFLAGS) -o writeRegister

.PHONY: clean
clean:
	rm -r readRegister readInputRegister writeRegister