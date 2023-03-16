# keithley_functions.py>

from pymeasure.instruments.keithley import Keithley2400  # Import the instrument of interest lib
import numpy as np
from time import sleep
from pymeasure.instruments import list_resources
import multiprocessing as mp
import time
import pandas as pd

global instruments_setup_values
global return_values


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


# The following function applys a list of continuous voltages,
# measure a list of continuous currents, and return this list of current
def Measure_List_Values_Current(sourcemeter_info):
    instrument_num = sourcemeter_info[0]
    sourcemeter = sourcemeter_info[1]
    voltage_value_list = sourcemeter_info[2]

    print("Instrument:", instrument_num," Time started:", time.time())

    sourcemeter.enable_source()
    current_value_list = np.zeros_like(voltage_value_list)
    for i in range(0, len(voltage_value_list)):
        sourcemeter.source_voltage = voltage_value_list[i]  # in Volt
        current_value_list[i] = sourcemeter.current
    sourcemeter.disable_source()

    return_values[instrument_num] = current_value_list

# ------------------- we have a Global value(dict): instruments_setup_values which contains the setup values
# ------------------- When you pass the instruments information from the UI to the BackEnd
# ------------------- the 1st object of this list is the instruments_setup_values
def Setup_Values(instruments_info):
    instruments_setup_values = instruments_info[0]
    print("\n")
    print("Setup Values-----------------")
    print(instruments_setup_values)


def Print_Instruments_info(instruments_info):
    print("\n")
    for instrument in instruments_info:
        print("Instrument-----------------")
        print(instrument)


def Setup_Instruments(instruments_info):
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


def Start_Instruments(sourcemeters):
    if __name__ == '__main__':
        for sourcemeter in sourcemeters:
            source_process = mp.Process(target=Measure_List_Values_Current, args=(sourcemeter,))
            source_process.start()


def Task_0_array(instruments_info):
    Setup_Values(instruments_info)
    instruments_info.pop(0)  # ------------------- remove the 1st element which contains the instruments_setup_values
    Print_Instruments_info(instruments_info)
    # ------------------- Here we Setup the instruments and ready execution
    sourcemeters = Setup_Instruments(instruments_info)
    # ------------------- Here we Start the measurements in parallel execution
    return_values = [[] for _ in range(len(sourcemeters))]
    Start_Instruments(sourcemeters)
    print(return_values)
    print("-----------\n")
    return "GOOD!"


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
