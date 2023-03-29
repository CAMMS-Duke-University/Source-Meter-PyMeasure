# keithley_functions.py>
from pymeasure.instruments.keithley import Keithley2400  # Import the instrument of interest lib
import numpy as np
import pandas as pd
from time import sleep
from pymeasure.instruments import list_resources
import time
from datetime import datetime


# ------------------- Here we search for the Instruments
def Get_Connected_Instruments():
    # return ["GPIB::01","GPIB::02","GPIB::03","GPIB::04","GPIB::05","GPIB::06","GPIB::07","GPIB::08"]
    connected_instrument_names = []
    for list_item in list_resources():
        connected_instrument_names.append(list_item)
    connected_instrument_names.pop(0)
    if len(connected_instrument_names) == 0:
        return ["N/A Connected"]
    else:
        return connected_instrument_names


# The following function connects and configure the scientific instrument
# returns the handler of this instrument as to use for start measuring voltage or current
def Instrument_Connection(instrument_name,  # Name Type and Port of Instrument
                          measure_operation,  # "Measure Voltage" or "Measure Current"
                          # ------------ for "Measure Current" Arguments
                          apply_voltage_range,  # in Volts
                          apply_compliance_current,  # in Amps
                          measure_current_nplc,  # Number of power line cycles (NPLC) from 0.01 to 10
                          measure_current,  # in Amps; Upper limit of current in Amps, from -1.05 A to 1.05 A
                          measure_current_auto_range,  # Enables auto_range if True, else uses the set resistance
                          # ------------ for "Measure Current" Arguments
                          apply_current_range,  # A current_range value or None
                          apply_compliance_voltage,  # A float in the correct range for a compliance_voltage
                          measure_voltage_nplc,  # Number of power line cycles (NPLC) from 0.01 to 10
                          measure_voltage,  # Upper limit of voltage in Volts, from -210 V to 210 V
                          measure_voltage_auto_range  # Enables auto_range if True, else uses the set voltage
                          ):
    sourcemeter = Keithley2400(instrument_name)
    sourcemeter.reset()
    sourcemeter.use_front_terminals()
    if measure_operation == "Measure Current":
        sourcemeter.apply_voltage(voltage_range=apply_voltage_range, compliance_current=apply_compliance_current)
        sourcemeter.measure_current(nplc=measure_current_nplc, current=measure_current,
                                    auto_range=measure_current_auto_range)
    if measure_operation == "Measure Voltage":
        sourcemeter.apply_current(current_range=apply_current_range, compliance_voltage=apply_compliance_voltage)
        sourcemeter.measure_voltage(nplc=measure_voltage_nplc, voltage=measure_voltage,
                                    auto_range=measure_voltage_auto_range)
    print(sourcemeter)
    sleep(0.1)  # wait here to give the instrument time to react
    return sourcemeter


# ------------------- we have a Global value(dict): instruments_setup_values which contains the setup values
# ------------------- When you pass the instruments information from the UI to the BackEnd
# ------------------- the 1st object of this list is the instruments_setup_values
def Setup_Values(instruments_info):
    instruments_setup_values = instruments_info[0]
    print("Setup Values .........")
    print(instruments_setup_values)
    return instruments_setup_values


def Print_Instruments_info(instruments_info):
    for instrument in instruments_info:
        print("Instruments .........")
        print(instrument)


def Setup_Instruments(instruments_setup_values, instruments_info):
    print("Setup Instruments .........")
    sourcemeters = []
    # ------------------- Here we Setup the Sourcemeter Instruments AND their process via the input data we will apply
    for instrument in instruments_info:
        print("Instrument ID: ", instrument["Instrument"], "- Port Number", instrument["Port Number"])
        instrument_optionmenu = instrument['OptionMenu']
        applied_values = []  # the values which will be applied
        measure_operation = None  # measure type are "Measure Voltage" or "Measure Current"
        # "Measure Current" corresponds to "Apply Incremental Voltage" & "Apply Steady Voltage"
        # "Measure Voltage" corresponds to "Apply Incremental Current" & "Apply Steady Current"
        if instrument_optionmenu == 'Apply Incremental Voltage':
            measure_operation = "Measure Current"
            applied_values = np.linspace(start=int(instrument['Min Voltage (Volts)']),
                                         stop=int(instrument['Max Voltage (Volts)']),
                                         num=int(instrument['Measurement Number']))
        if instrument_optionmenu == 'Apply Steady Voltage':
            measure_operation = "Measure Current"
            applied_values = np.linspace(start=int(instrument['Steady Voltage (Volts)']),
                                         stop=int(instrument['Steady Voltage (Volts)']),
                                         num=int(instrument['Measurement Number']))
        if instrument_optionmenu == 'Apply Incremental Current':
            measure_operation = "Measure Voltage"
            applied_values = np.linspace(start=float(instrument['Min Current (Amps)']),
                                         stop=float(instrument['Max Current (Amps)']),
                                         num=int(instrument['Measurement Number']))
        if instrument_optionmenu == 'Apply Steady Current':
            measure_operation = "Measure Voltage"
            applied_values = np.linspace(start=float(instrument['Steady Current (Amps)']),
                                         stop=float(instrument['Steady Current (Amps)']),
                                         num=int(instrument['Measurement Number']))
        print("Measure Option:", measure_operation)
        print("Applied Values:", applied_values)
        sourcemeter = Instrument_Connection(instrument_name=instrument['Port Number'],
                                            measure_operation=measure_operation,
                                            # ------------ for "Measure Current" Arguments
                                            apply_voltage_range=None if instruments_setup_values[
                                                                            "Voltage Range [Measure Current]"] == 'None' else float(
                                                instruments_setup_values["Voltage Range [Measure Current]"]),  # =None,
                                            apply_compliance_current=float(
                                                instruments_setup_values["Compliance Current [Measure Current]"]),
                                            # =10e-4,
                                            measure_current_nplc=int(
                                                instruments_setup_values["Power Line Cycles [Measure Current]"]),  # =1,
                                            measure_current=float(
                                                instruments_setup_values["Current Range [Measure Current]"]),
                                            # =0.000105,
                                            measure_current_auto_range=bool(
                                                instruments_setup_values["Auto Range [Measure Current]"]),  # =True
                                            # ------------ for "Measure Current" Arguments
                                            apply_current_range=None if instruments_setup_values[
                                                                            "Current Range [Measure Voltage]"] == 'None' else float(
                                                instruments_setup_values["Current Range [Measure Voltage]"]),  # =None,
                                            apply_compliance_voltage=float(
                                                instruments_setup_values["Compliance Voltage [Measure Voltage]"]),
                                            # 0.1,
                                            measure_voltage_nplc=int(
                                                instruments_setup_values["Power Line Cycles [Measure Voltage]"]),  # =1,
                                            measure_voltage=float(
                                                instruments_setup_values["Voltage Range [Measure Voltage]"]),  # 21.0,
                                            measure_voltage_auto_range=bool(
                                                instruments_setup_values["Auto Range [Measure Voltage]"]))  # True)
        sourcemeters.append((instrument["Port Number"], sourcemeter, applied_values, measure_operation))
    return sourcemeters


# The following function apply a list of continuous voltages,
# measure a list of continuous currents, and return this list of current
def Measure_Multi_Instruments(sourcemeters_info):
    # the Argument sourcemeters_info is a list of lists: a 2-D list
    # the outer list corresponds to the used Instruments, each item of the outer list refers to a sole Instrument object
    # each Instrument object (inner list) contains the following items:
    # item 0 => [Instrument][0]: Instrument ID,
    # item 1 => [Instrument][1]: Keithley2400 sourcemeter connection reference/pointer
    # item 2 => [Instrument][2]: list of input values of this Instrument,
    # item 3 => [Instrument][3]: measure_operation, if the Instrument Apply Voltage and Measure Current or the opposite
    instruments_num = len(sourcemeters_info)  # Number of used Instruments
    values_size = len(sourcemeters_info[0][2])
    for i in range(0, instruments_num):
        if len(sourcemeters_info[i][2]) < values_size:
            values_size = len(sourcemeters_info[i][2])  # Because is parallel take the smaller Number of Measurements
    # --------- Initiate
    sourcemeters = []  # we create a list of the reference/pointer for each sourcemeter
    applied_values = []  # we create a 2-D array; each row is the Instrument; each column is the parallel applied value
    measured_values = []  # we create a 2-D array; each row is the Instrument; each column is the parallel measured value
    measure_operations = []  # we create a list of the operations for each sourcemeter if measure Current or Voltage
    for i in range(0, instruments_num):
        sourcemeters.append(sourcemeters_info[i][1])
        applied_values.append(sourcemeters_info[i][2])
        measured_values.append(np.zeros(values_size))
        measure_operations.append(sourcemeters_info[i][3])
    applied_values = np.array(applied_values)
    measured_values = np.array(measured_values)
    # --------- Enable sourcemeters
    for sourcemeter in sourcemeters:
        sourcemeter.enable_source()
    # --------- Measure
    for i in range(0, values_size):
        for j in range(0, instruments_num):  # Parallel
            current_sourcemeter = sourcemeters[j]
            current_measure_operation = measure_operations[j]
            current_applied_value = applied_values[j, i]
            if current_measure_operation == "Measure Current":
                current_sourcemeter.source_voltage = current_applied_value
                measured_values[j, i] = current_sourcemeter.current
            elif current_measure_operation == "Measure Voltage":
                current_sourcemeter.source_current = current_applied_value
                measured_values[j, i] = current_sourcemeter.voltage
        time.sleep(0.25)
    # --------- Disable sourcemeters
    for sourcemeter in sourcemeters:
        sourcemeter.disable_source()
    # --------- Construct the results in tuples (applied values, measured values) for each instrument
    my_results = []
    for i in range(0, instruments_num):
        my_results.append((list(applied_values[i]), list(measured_values[i])))
        # print("------------Instrument:", i+1)
        # print(" Applied Values:", applied_values[i])
        # print(" Measured Values:", measured_values[i])
    return (my_results)


def Start_Instruments_Parallel(sourcemeters):
    if len(sourcemeters) >= 1:
        print("Start Measure .........")
        return_values = Measure_Multi_Instruments(sourcemeters)
        return return_values
    else:
        print("No Instruments are selected")
        return None


def Store_Data(result_values, instruments_info):
    instruments_num = len(result_values)
    result_values_and_info = []
    for i in range(0, instruments_num):
        curr_port_number = instruments_info[i]['Port Number']
        curr_applied_values = result_values[i][0]
        curr_measured_values = result_values[i][1]
        print("----------------------")
        print("Instrument:", curr_port_number, "Applied Values:",curr_applied_values, "Measured Values:", curr_measured_values)
        curr_values_and_info = (curr_port_number, curr_applied_values, curr_measured_values)
        result_values_and_info.append(curr_values_and_info)
    # print(result_values_and_info)
    # datetime object containing current date and time
    now = datetime.now()
    pd.DataFrame(result_values_and_info).to_csv("data/Results-"+ str(now.strftime("%d-%m-%Y-%H:%M:%S")) + ".csv")
    print("...Saved")


def Task_0_array(instruments_info):
    instruments_setup_values = Setup_Values(instruments_info)
    instruments_info.pop(0)  # ------------------- remove the 1st element which contains the instruments_setup_values
    Print_Instruments_info(instruments_info)
    # ------------------- Here we Setup the instruments and ready execution
    sourcemeters = Setup_Instruments(instruments_setup_values, instruments_info)
    # print("Sourcemeter:",sourcemeters)
    # ------------------- Here we Start the measurements in parallel execution
    # return_values = Start_Instruments_Sequential(sourcemeters)
    return_values = Start_Instruments_Parallel(sourcemeters) # is a list of tuples (applied_values, measured_values)
    # print("Returned Values:",return_values)
    Store_Data(return_values, instruments_info)

    print("-----------\n")
    return "GOOD!"
