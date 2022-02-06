CXX = g++
CXXFLAGS = -std=c++11 -I /usr/include/modbus -lmodbus -lpthread

DEPS = fan.hpp
OBJ = fan.o main.o 

%.o: %.c $(DEPS)
	$(CXX) -c -o $@ $< $(CXXFLAGS)

main: $(OBJ)
	$(CXX) -o $@ $^ $(CXXFLAGS)


.PHONY: clean
clean:
	rm -r main.o