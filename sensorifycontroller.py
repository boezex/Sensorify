import pressuresensor
import gui
import config
import fan
import measurementcontroller

conf = config.Config ()
mainFan = fan.Fan ()

sens = pressuresensor.PressureSensor ()
msmcontroller = measurementcontroller.MeasurementController ()
interface = gui.GUI (sens, conf, mainFan)

mainFan.setGUI (interface)

print(sens.readPressure())
interface.run ()