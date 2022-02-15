import pressuresensor
import gui
import config

conf = config.Config ()

sens = pressuresensor.PressureSensor ()
interface = gui.GUI (sens, conf)

print(sens.readPressure())
interface.run ()