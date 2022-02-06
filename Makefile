CXX = g++
CXXFLAGS = -std=c++11 -I /usr/include/modbus -lmodbus -lpthread

main: main.o fan.o
	$(CXX) $(CXXFLAGS) -o main main.o fan.o

main.o: main.cpp fan.hpp
	$(CXX) $(CXXFLAGS) -c main.cpp

fan.o: fan.hpp
	$(CXX) $(CXXFLAGS) -c fan.cpp


.PHONY: clean
clean:
	rm -r main.o