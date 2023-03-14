# keithley_functions.py>

from pymeasure.instruments.keithley import Keithley2400  # Import the instrument of interest lib
import numpy as np
import pandas as pd
from time import sleep
from pymeasure.instruments import list_resources

global apply_voltage_range_val
global apply_compliance_current_val
global apply_nplc_val
global apply_current_range_val
global apply_auto_range_val

global instruments_setup_values

# The following function connects and configure the scientific instrument
# returns the handler of this instrument as to use for start measuring voltage or current
def Instrument_Connection(instrument_name,  # Name Type and Port of Instrument
                          apply_voltage_range,  # in Volts
                          apply_compliance_current,  # in Amps
                          apply_nplc,  # Number of power line cycles (NPLC) from 0.01 to 10
                          apply_current_range,  # in Amps; Upper limit of current in Amps, from -1.05 A to 1.05 A
                          apply_auto_range):  # Enables auto_range if True, else uses the set resistance
    sourcemeter = Keithley2400(instrument_name)
    sourcemeter.reset()
    sourcemeter.use_front_terminals()
    sourcemeter.apply_voltage(voltage_range=apply_voltage_range, compliance_current=apply_compliance_current)
    sourcemeter.measure_current(nplc=apply_nplc, current=apply_current_range, auto_range=apply_auto_range)
    sleep(0.1)  # wait here to give the instrument time to react
    return (sourcemeter)


# The following function applys one voltage, measures one current, and returns this current value
def Measure_Single_Value_Current(sourcemeter, voltage_value):
    sourcemeter.enable_source()
    sourcemeter.source_voltage = voltage_value  # in Volt
    current_value = sourcemeter.current
    sourcemeter.disable_source()
    return (current_value)


# The following function applys a list of continuous voltages,
# measure a list of continuous currents, and return this list of current
def Measure_List_Values_Current(sourcemeter, voltage_value_list):
    sourcemeter.enable_source()
    current_value_list = np.zeros_like(voltage_value_list)
    for i in range(0, len(voltage_value_list)):
        sourcemeter.source_voltage = voltage_value_list[i]  # in Volt
        current_value_list[i] = sourcemeter.current
    sourcemeter.disable_source()
    return (current_value_list)


# The following functions operates two GPIBs
# (1) applys a DC Voltage to the first GPIB and measures the current
# (2) applys a gradually increased voltage and measures the current
# (3) returns the 2 lists of Cureents
def Task_1(instrument_A_name,
           instrument_B_name,
           apply_voltage_range,
           apply_compliance_current,
           apply_nplc,
           apply_current_range,
           apply_auto_range,
           number_of_measurements,
           dc_voltage,
           ac_min_voltage,
           ac_max_voltage):
    sourcemeter_A = Instrument_Connection(instrument_A_name,
                                          apply_voltage_range,
                                          apply_compliance_current,
                                          apply_nplc,
                                          apply_current_range,
                                          apply_auto_range)
    sourcemeter_B = Instrument_Connection(instrument_B_name,
                                          apply_voltage_range,
                                          apply_compliance_current,
                                          apply_nplc,
                                          apply_current_range,
                                          apply_auto_range)
    voltages_sourcemeter_A = np.linspace(dc_voltage, dc_voltage, num=number_of_measurements)
    voltages_sourcemeter_B = np.linspace(ac_min_voltage, ac_max_voltage, num=number_of_measurements)
    currents_sourcemeter_A = Measure_List_Values_Current(sourcemeter_A, voltages_sourcemeter_A)
    currents_sourcemeter_B = Measure_List_Values_Current(sourcemeter_B, voltages_sourcemeter_B)
    return (currents_sourcemeter_A, currents_sourcemeter_B)


# function
def Task_1_array(entries):
    print("\n")
    print(entries)
    print("\n")
    instrument_A_name = entries[0]
    instrument_B_name = entries[1]
    apply_voltage_range = None if entries[2] == "None" else float(entries[2])
    apply_compliance_current = float(entries[3])
    apply_nplc = int(entries[4])
    apply_current_range = float(entries[5])
    apply_auto_range = bool(entries[6])
    number_of_measurements = int(entries[7])
    dc_voltage = int(entries[8])
    ac_min_voltage = int(entries[9])
    ac_max_voltage = int(entries[10])
    sourcemeter_A = Instrument_Connection(instrument_A_name,
                                          apply_voltage_range,
                                          apply_compliance_current,
                                          apply_nplc,
                                          apply_current_range,
                                          apply_auto_range)
    sourcemeter_B = Instrument_Connection(instrument_B_name,
                                          apply_voltage_range,
                                          apply_compliance_current,
                                          apply_nplc,
                                          apply_current_range,
                                          apply_auto_range)
    voltages_sourcemeter_A = np.linspace(dc_voltage, dc_voltage, num=number_of_measurements)
    voltages_sourcemeter_B = np.linspace(ac_min_voltage, ac_max_voltage, num=number_of_measurements)
    currents_sourcemeter_A = Measure_List_Values_Current(sourcemeter_A, voltages_sourcemeter_A)
    currents_sourcemeter_B = Measure_List_Values_Current(sourcemeter_B, voltages_sourcemeter_B)
    return (currents_sourcemeter_A, currents_sourcemeter_B)


def Task_0_array(instruments):
    print("\n")
    instruments_setup_values = instruments[0]
    print("Setup Values-----------------")
    print(instruments_setup_values)
    instruments.pop(0)
    for instrument in instruments:
        print("Instument-----------------")
        print(instrument)
    # return None

    sourcemeters = []
    # ------------------- We setup the Sourcemeter Instruments AND their process via the input data we will apply
    for instrument in instruments:
        print(instrument)
        print("Instrument ID: ", instrument["Instrument"])
        sourcemeter = Instrument_Connection(instrument_name=instrument['Port Number'],
                                            apply_voltage_range= None if instruments_setup_values["Voltage Range"]=='None' else float(instruments_setup_values["Voltage Range"]), # =None,
                                            apply_compliance_current=float(instruments_setup_values["Compliance Current"]), # =10e-4,
                                            apply_nplc= int(instruments_setup_values["Power Line Cycles"]), # =1,
                                            apply_current_range= float(instruments_setup_values["Current Range"]), #=0.000105,
                                            apply_auto_range= bool(instruments_setup_values["Auto Range"])) #=True)
        instrument_optionmenu = instrument['OptionMenu']
        if instrument_optionmenu == 'Apply Incremental Voltage':
            voltages_sourcemeter = np.linspace(start=int(instrument['Min Voltage (Volts)']),
                                               stop=int(instrument['Max Voltage (Volts)']),
                                               num=int(instrument['Measurement Number']))
        if instrument_optionmenu == 'Apply Steady Voltage':
            voltages_sourcemeter = np.linspace(start=int(instrument['Steady Voltage (Volts)']),
                                               stop=int(instrument['Steady Voltage (Volts)']),
                                               num=int(instrument['Measurement Number']))
        sourcemeters.append((sourcemeter, voltages_sourcemeter))

    currents = []
    for sourcemeter in sourcemeters:
        current = Measure_List_Values_Current(sourcemeter[0], sourcemeter[1])
        currents.append(current)
    print(currents)
    print("-----------\n")
    return "GOOD!"


def Get_Connected_Instruments():
    # return ["GPIB::01","GPIB::02","GPIB::03","GPIB::04","GPIB::05","GPIB::06","GPIB::07","GPIB::08"]
    connected_instrument_names = []
    for list_item in list_resources():
        connected_instrument_names.append(list_item)
    connected_instrument_names.pop(0)
    if (len(connected_instrument_names) == 0):
        return "No Instrument is connected"
    else:
        return connected_instrument_names
