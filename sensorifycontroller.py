import pressuresensor
import gui
import config
import fan
import measurementcontroller

conf = config.Config ()
mainFan = fan.Fan ()

sens = pressuresensor.PressureSensor ()
msmcontroller = measurementcontroller.MeasurementController (mainFan, sens, conf)
interface = gui.GUI (sens, conf, mainFan, msmcontroller)

mainFan.setGUI (interface)
msmcontroller.setGUI (interface)

print(sens.readPressure())
interface.run ()