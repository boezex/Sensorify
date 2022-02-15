CXX = g++
CXXFLAGS = -std=c++11 -I /usr/include/modbus -lmodbus -lpthread

main: readregister readinputregister writeregister
	@echo appaatjes worden gebouwd
	chmod +x readRegister readInputRegister writeRegister


readregister: readRegister.cpp
	$(CXX) $(CXXFLAGS) -c readRegister.cpp -o readRegister

readinputregister: readInputRegister.cpp
	$(CXX) $(CXXFLAGS) -c readInputRegister.cpp -o readInputRegister

writeregister: writeRegister.cpp
	$(CXX) $(CXXFLAGS) -c writeRegister.cpp -o writeRegister

.PHONY: clean
clean:
	rm -r readRegister readInputRegister writeRegister