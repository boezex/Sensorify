import pressuresensor
import gui
import config

conf = config.Config ()
conf.setDefaults ()

sens = pressuresensor.PressureSensor ()
interface = gui.GUI (sens, conf)

print(sens.readPressure())