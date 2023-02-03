# First import the instrument of interest.
from pymeasure.instruments.keithley import Keithley2400
# Import necessary packages
import numpy as np
import pandas as pd
from time import sleep

# Set source_current and measure_voltage parameters
current_range = 10e-3  # in Amps
compliance_voltage = 10  # in Volts
measure_nplc = 0.1  # Number of power line cycles
voltage_range = 1  # in VOlts

# Connect and configure the instrument
sourcemeter = Keithley2400("GPIB::3")
sourcemeter.reset()
sourcemeter.use_front_terminals()
sourcemeter.apply_current(current_range, compliance_voltage)
sourcemeter.measure_voltage(measure_nplc, voltage_range)
sleep(0.1)  # wait here to give the instrument time to react
sourcemeter.stop_buffer()
sourcemeter.disable_buffer()

# Set the input parameters
data_points = 10
averages = 10
max_current = 0.001
min_current = -max_current

# Allocate arrays to store the measurement results
currents = np.linspace(min_current, max_current, num=data_points)
voltages = np.zeros_like(currents)
voltage_stds = np.zeros_like(currents)

print("Init Currents:",currents)
print("Init Voltages:",voltages)
print("Init stds Voltages:",voltage_stds)

sourcemeter.enable_source()


# Loop through each current point, measure and record the voltage
for i in range(data_points):
    sourcemeter.config_buffer(averages)
    sourcemeter.source_current = currents[i]
    sourcemeter.start_buffer()
    sourcemeter.wait_for_buffer()
    # Record the average and standard deviation
    voltages[i] = sourcemeter.means[0]
    sleep(1.0)
    voltage_stds[i] = sourcemeter.standard_devs[0]

print(currents, voltages, voltage_stds)

sourcemeter.shutdown()
