import pressuresensor
import gui
import config
import fan

conf = config.Config ()
mainFan = fan.Fan ()

sens = pressuresensor.PressureSensor ()
interface = gui.GUI (sens, conf, mainFan)

mainFan.setGUI (interface)

print(sens.readPressure())
interface.run ()