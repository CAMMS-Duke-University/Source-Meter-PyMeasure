# keithley_functions.py>
from pymeasure.instruments.keithley import Keithley2400  # Import the instrument of interest lib
import numpy as np
import pandas as pd
from time import sleep
from pymeasure.instruments import list_resources
import time


def Get_Connected_Instruments():
    # return ["GPIB::01","GPIB::02","GPIB::03","GPIB::04","GPIB::05","GPIB::06","GPIB::07","GPIB::08"]
    connected_instrument_names = []
    for list_item in list_resources():
        connected_instrument_names.append(list_item)
    connected_instrument_names.pop(0)
    if len(connected_instrument_names) == 0:
        return "No Instrument is connected"
    else:
        return connected_instrument_names


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


# ------------------- we have a Global value(dict): instruments_setup_values which contains the setup values
# ------------------- When you pass the instruments information from the UI to the BackEnd
# ------------------- the 1st object of this list is the instruments_setup_values
def Setup_Values(instruments_info):
    instruments_setup_values = instruments_info[0]
    print("\n")
    print("Setup Values-----------------")
    print(instruments_setup_values)
    return instruments_setup_values


def Print_Instruments_info(instruments_info):
    print("\n")
    for instrument in instruments_info:
        print("Instrument-----------------")
        print(instrument)


def Setup_Instruments(instruments_setup_values, instruments_info):
    sourcemeters = []
    # ------------------- Here we Setup the Sourcemeter Instruments AND their process via the input data we will apply
    for instrument in instruments_info:
        print("Instrument ID: ", instrument["Instrument"])
        sourcemeter = Instrument_Connection(instrument_name=instrument['Port Number'],
                                            apply_voltage_range=None if instruments_setup_values[
                                                                            "Voltage Range"] == 'None' else float(
                                                instruments_setup_values["Voltage Range"]),  # =None,
                                            apply_compliance_current=float(
                                                instruments_setup_values["Compliance Current"]),  # =10e-4,
                                            apply_nplc=int(instruments_setup_values["Power Line Cycles"]),  # =1,
                                            apply_current_range=float(instruments_setup_values["Current Range"]),
                                            # =0.000105,
                                            apply_auto_range=bool(instruments_setup_values["Auto Range"]))  # =True)
        instrument_optionmenu = instrument['OptionMenu']
        if instrument_optionmenu == 'Apply Incremental Voltage':
            voltages_sourcemeter = np.linspace(start=int(instrument['Min Voltage (Volts)']),
                                               stop=int(instrument['Max Voltage (Volts)']),
                                               num=int(instrument['Measurement Number']))
        if instrument_optionmenu == 'Apply Steady Voltage':
            voltages_sourcemeter = np.linspace(start=int(instrument['Steady Voltage (Volts)']),
                                               stop=int(instrument['Steady Voltage (Volts)']),
                                               num=int(instrument['Measurement Number']))
        sourcemeters.append((instrument["Instrument"], sourcemeter, voltages_sourcemeter))
    return sourcemeters


# The following function applys a list of continuous voltages,
# measure a list of continuous currents, and return this list of current
def Measure_Current_Single_Instrument(sourcemeter_info):
    instrument_num = sourcemeter_info[0]
    sourcemeter = sourcemeter_info[1]
    voltage_value_list = sourcemeter_info[2]

    sourcemeter.enable_source()
    current_value_list = np.zeros_like(voltage_value_list)
    for i in range(0, len(voltage_value_list)):
        sourcemeter.source_voltage = voltage_value_list[i]  # in Volt
        current_value_list[i] = sourcemeter.current
    sourcemeter.disable_source()
    return (current_value_list)


def Start_Instruments_Sequential(sourcemeters):
    return_values = []
    for sourcemeter in sourcemeters:
        return_values.append(Measure_Current_Single_Instrument(sourcemeter))
    return (return_values)


# 2 Instruments: The following function applys a list of continuous voltages,
# measure a list of continuous currents, and return this list of current
def Measure_Current_Multi_Instruments(sourcemeters_info):
    instruments_num = len(sourcemeters_info)
    values_size = len(sourcemeters_info[0][2])
    # --------- Initiate
    sourcemeters = []
    voltage_values = []
    current_values = []
    for i in range(0, instruments_num):
        sourcemeters.append(sourcemeters_info[i][1])
        voltage_values.append(sourcemeters_info[i][2])
        current_values.append(np.zeros(values_size))
    # --------- Enable sourcemeters
    for sourcemeter in sourcemeters:
        sourcemeter.enable_source()
    # --------- Measure
    for i in range(0, values_size):
        for j in range(0, instruments_num): # Parallel
            current_sourcemeter = sourcemeters[j]
            current_voltage_value = voltage_values[j,i]
            current_sourcemeter.source_voltage = current_voltage_value
            current_values[j, i] = current_sourcemeter.current
        time.sleep(0.25)
    # --------- Disable sourcemeters
        for sourcemeter in sourcemeters:
            sourcemeter.disable_source()
    # --------- Print Currents
    for i in (0, instruments_num):
        print("Current Instrument",i+1,":",current_values[i])
    return (current_values)


def Measure_Current_Two_Instruments(sourcemeters_info):
    instrument_num_1 = sourcemeters_info[0][0]
    sourcemeter_1 = sourcemeters_info[0][1]
    voltage_value_list_1 = sourcemeters_info[0][2]

    instrument_num_2 = sourcemeters_info[1][0]
    sourcemeter_2 = sourcemeters_info[1][1]
    voltage_value_list_2 = sourcemeters_info[1][2]

    sourcemeter_1.enable_source()
    sourcemeter_2.enable_source()
    current_value_list_1 = np.zeros_like(voltage_value_list_1)
    current_value_list_2 = np.zeros_like(voltage_value_list_2)
    for i in range(0, len(voltage_value_list_1)):
        sourcemeter_1.source_voltage = voltage_value_list_1[i]  # in Volt
        current_value_list_1[i] = sourcemeter_1.current
        sourcemeter_2.source_voltage = voltage_value_list_2[i]  # in Volt
        current_value_list_2[i] = sourcemeter_2.current
        time.sleep(0.25)
    sourcemeter_1.disable_source()
    sourcemeter_2.disable_source()
    print("Current Iinst 1:", current_value_list_1)
    print("Current Iinst 2:", current_value_list_2)
    return (current_value_list_1 + current_value_list_2)


def Start_Instruments_Parallel(sourcemeters):
    if (len(sourcemeters) == 2):
        print("Use 2 Instruments Simultaneously")
        return_values = Measure_Current_Two_Instruments(sourcemeters)
        return (sourcemeters)


def Task_0_array(instruments_info):
    instruments_setup_values = Setup_Values(instruments_info)
    instruments_info.pop(0)  # ------------------- remove the 1st element which contains the instruments_setup_values
    Print_Instruments_info(instruments_info)
    # ------------------- Here we Setup the instruments and ready execution
    sourcemeters = Setup_Instruments(instruments_setup_values, instruments_info)
    print(sourcemeters)
    # ------------------- Here we Start the measurements in parallel execution
    # return_values = Start_Instruments_Sequential(sourcemeters)
    return_values = Start_Instruments_Parallel(sourcemeters)
    # print(return_values)
    print("-----------\n")
    return "GOOD!"
