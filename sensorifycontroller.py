import pressuresensor
import gui
import config
import fan
import measurementcontroller

conf = config.Config ()
mainFan = fan.Fan ()

sens = pressuresensor.PressureSensor ()
msmcontroller = measurementcontroller.MeasurementController (mainFan, sens)
interface = gui.GUI (sens, conf, mainFan, msmcontroller)

mainFan.setGUI (interface)

print(sens.readPressure())
interface.run ()