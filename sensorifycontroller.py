import pressuresensor
import gui


sens = pressuresensor.PressureSensor()
interface = gui.GUI(sens)

print(sens.readPressure())