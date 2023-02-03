import pymeasure
print("PyMeasure version:", pymeasure.__version__)

from pymeasure.instruments import list_resources
print(list_resources())
print("-----")

# First import the instrument of interest.
from pymeasure.instruments.keithley import Keithley2400

sourcemeter_A = Keithley2400("GPIB::3")
#----- Way 1
print("Keithley2410 info:",sourcemeter_A.id)
#----- Way 2
print("Asked:",sourcemeter_A.ask("*IDN?"))
#----- Way 3
sourcemeter_A.write("*IDN?")
print("Asked:",sourcemeter_A.read())

print("-----")
sourcemeter_B = Keithley2400("GPIB::3")
#----- Way 1
print("Keithley2410 info:",sourcemeter_B.id)
#----- Way 2
print("Asked:",sourcemeter_B.ask("*IDN?"))
#----- Way 3
sourcemeter_B.write("*IDN?")
print("Asked:",sourcemeter_B.read())
