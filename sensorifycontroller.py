import pressuresensor
import gui
import config
import fan

conf = config.Config ()
fannetje = fan.Fan ()

sens = pressuresensor.PressureSensor ()
interface = gui.GUI (sens, conf)

fannetje.setGUI (interface)

print(sens.readPressure())
interface.run ()