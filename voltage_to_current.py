"""
Appy Voltage measure a Current
"""

# Import the instrument of interest.
from pymeasure.instruments.keithley import Keithley2400
# Import additional packages
import numpy as np
import pandas as pd
from time import sleep


instrument_name = "GPIB::3"
apply_voltage_range = None # in Volts
apply_compliance_current = 10e-4 # in Amps
apply_nplc = 1 # Number of power line cycles (NPLC) from 0.01 to 10
apply_current_range = 0.000105 # in Amps; Upper limit of current in Amps, from -1.05 A to 1.05 A
apply_auto_range = True

# Connect and configure the instrument
def Instrument_Connection (instrument_name, # Name Type and Port of Instrument
                           apply_voltage_range, # in Volts
                           apply_compliance_current, # in Amps
                           apply_nplc, # Number of power line cycles (NPLC) from 0.01 to 10
                           apply_current_range, # in Amps; Upper limit of current in Amps, from -1.05 A to 1.05 A
                           apply_auto_range): # Enables auto_range if True, else uses the set resistance
    sourcemeter = Keithley2400(instrument_name)
    sourcemeter.reset()
    sourcemeter.use_front_terminals()
    sourcemeter.apply_voltage(voltage_range=apply_voltage_range, compliance_current=apply_compliance_current)
    sourcemeter.measure_current(nplc=apply_nplc, current=apply_current_range, auto_range=apply_auto_range)
    sleep(0.1)  # wait here to give the instrument time to react
    return(sourcemeter)

# The following function applys one voltage and measures one current
def Measure_Single_Value_Current(sourcemeter,voltage_value):
    sourcemeter.enable_source()
    sourcemeter.source_voltage = voltage_value # in Volt
    current_value = sourcemeter.current
    sourcemeter.disable_source()
    return(current_value)

# The following function applys a list of continuous voltages and measure a list of continuous currents
def Measure_List_Values_Current(sourcemeter,voltage_value_list):
    sourcemeter.enable_source()
    current_value_list = np.zeros_like(voltage_value_list)
    for i in range(0,len(voltage_value_list)):
        sourcemeter.source_voltage = voltage_value_list[i] # in Volt
        current_value_list[i] = sourcemeter.current
    sourcemeter.disable_source()
    return(current_value_list)

"""
sourcemeter = Instrument_Connection ("GPIB::3", None, 10e-4, 1, 0.000105, True)
current = Measure_Single_Value_Current(sourcemeter,1)
print(current)

min_voltage = 1
max_voltage = 10
data_points = 10
voltages = np.linspace(min_voltage, max_voltage, num=data_points)
currents = Measure_List_Values_Current(sourcemeter,voltages)
print(currents)
"""

def Task_1 (number_of_measurements,dc_voltage, ac_min_voltage, ac_max_voltage):
    sourcemeter_A = Instrument_Connection ("GPIB::3", None, 10e-4, 1, 0.000105, True)
    sourcemeter_B = Instrument_Connection ("GPIB::6", None, 10e-4, 1, 0.000105, True)
    voltages_sourcemeter_A = np.linspace(dc_voltage, dc_voltage, num=number_of_measurements)
    voltages_sourcemeter_B = np.linspace(ac_min_voltage, ac_max_voltage, num=number_of_measurements)
    currents_sourcemeter_A = Measure_List_Values_Current(sourcemeter_A,voltages_sourcemeter_A)
    currents_sourcemeter_B = Measure_List_Values_Current(sourcemeter_B,voltages_sourcemeter_B)
    return(currents_sourcemeter_A,currents_sourcemeter_B)


currents_A, currents_B = Task_1 (10,1, 1, 10)
print("First:",currents_A)
print("Second:",currents_B)

"""



#------------
sourcemeter.enable_source()
sourcemeter.source_voltage = 1 # in Volt
print(sourcemeter.current)
sourcemeter.disable_source()
#-------------

# Set the input parameters
data_points = 10
averages = 0.5
max_voltage = 1
min_voltage = 0




# Allocate arrays to store the measurement results
voltages = np.linspace(min_voltage, max_voltage, num=data_points)
print("Init Voltages:",voltages)
currents = np.zeros_like(voltages)
current_stds = np.zeros_like(voltages)
print("Init Currents:",currents)
print("Init stds Currents:",current_stds)

sourcemeter.enable_source()

# Loop through each current point, measure and record the voltage
for i in range(data_points):
    #sourcemeter.config_buffer(currents)
    sourcemeter.source_voltage = voltages[i]
    #sourcemeter.start_buffer()
    sourcemeter.wait_for_buffer()
    # Record the average and standard deviation
    currents[i] = sourcemeter.means[0]
    sleep(1.0)
    current_stds[i] = sourcemeter.standard_devs[0]

print(voltages, currents, current_stds)

sourcemeter.shutdown()
"""
