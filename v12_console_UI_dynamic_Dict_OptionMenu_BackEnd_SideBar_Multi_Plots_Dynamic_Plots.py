import tkinter
import tkinter.messagebox
from tkinter import filedialog as fd
import customtkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import pyplot as plt, animation
from pymeasure.instruments.keithley import Keithley2400  # Import the instrument of interest lib
import numpy as np
import pandas as pd
from time import sleep
from pymeasure.instruments import list_resources
import time
from datetime import datetime

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

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
def Measure_Multi_Instruments(sourcemeters_info, time_step):
    # the Argument sourcemeters_info is a list of lists: a 2-D list
    # the outer list corresponds to the used Instruments, each item of the outer list refers to a sole Instrument object
    # each Instrument object (inner list) contains the following items:
    # item 0 => [Instrument][0]: Instrument ID,
    # item 1 => [Instrument][1]: Keithley2400 sourcemeter connection reference/pointer
    # item 2 => [Instrument][2]: list of input values of this Instrument,
    # item 3 => [Instrument][3]: measure_operation, if the Instrument Apply Voltage and Measure Current or the opposite
    instruments_num = len(sourcemeters_info)  # Number of used Instruments
    # --------- Initiate
    values_size = len(sourcemeters_info[0][2])
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
    timestamps = []
    time_init = datetime.now()
    for i in range(0, values_size):
        # --------- take timer
        now = datetime.now()
        time_difference = now - time_init
        # print(time_difference, type(time_difference),str(time_difference)[2:])
        timestamps.append(str(time_difference)[2:])
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
        time.sleep(time_step)
    # print(timestamps)
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
    return my_results, timestamps


def Start_Instruments_Parallel(sourcemeters, time_step):
    if len(sourcemeters) >= 1:
        print("Start Measure .........")
        return_values, timestamps = Measure_Multi_Instruments(sourcemeters, time_step)
        return return_values, timestamps
    else:
        print("No Instruments are selected")
        return None


def Store_Data_Rows(result_values, instruments_info):
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

def Create_SCV_Columns(instruments_info):
    csv_columns = ['Time (min)']
    for instrument in instruments_info:
        instrument_port = instrument['Port Number']
        if instrument["OptionMenu"] == "Apply Steady Voltage":
            csv_columns.append(instrument_port + ' Voltage Set')
            csv_columns.append(instrument_port + ' Current Measure')
        if instrument["OptionMenu"] == "Apply Incremental Voltage":
            csv_columns.append(instrument_port + ' Voltage Set')
            csv_columns.append(instrument_port + ' Current Measure')
        if instrument["OptionMenu"] == "Apply Steady Current":
            csv_columns.append(instrument_port + ' Current Set')
            csv_columns.append(instrument_port + ' Voltage Measure')
        if instrument["OptionMenu"] == "Apply Incremental Current":
            csv_columns.append(instrument_port + ' Current Set')
            csv_columns.append(instrument_port + ' Voltage Measure')
    #print(csv_columns)
    return csv_columns

def Store_Data(result_values, instruments_info, time_step, timestamps):
    # result_values shape: Instrument X Applied-or-Measured X Measurement
    result_values = np.array(result_values)
    print("Results Shape:",result_values.shape)
    instruments_num = len(result_values)
    print("Instruments Num:", instruments_num)
    measurements_num = len(result_values[0][0])
    print("Measurements Num:",measurements_num)
    final_result_values = [[0]*(2*instruments_num+1)]*measurements_num
    final_result_values = np.float64(final_result_values)
    #-------------- First column is the time starting with Zero and increses with time_step
    for t in range(0,measurements_num):
        time_value_string = timestamps[t] # '00:00.000017'
        min_time_value = float(time_value_string[0:2])
        sec_min_time_value = float(time_value_string[3:])
        # print(time_value_string)
        # print("min:",min_time_value,"sec:",sec_min_time_value)
        final_result_values[t,0] = min_time_value + sec_min_time_value/60
    #-------------- Reshape Data
    final_result_values_column_counter = 1
    for i in range(0, instruments_num):
        for j in range(0, 2):
            for k in range(0,measurements_num):
                final_result_values[k,final_result_values_column_counter] = result_values[i,j,k]
                # print(k,final_result_values_column_counter,"<--",i,j,k, "Values:", result_values[i,j,k])
            final_result_values_column_counter +=1
    final_result_columns = Create_SCV_Columns(instruments_info)
    now = datetime.now()
    df = pd.DataFrame(final_result_values, columns=final_result_columns)
    df.to_csv("data/Results-"+ str(now.strftime("%d-%m-%Y-%H:%M:%S")) + ".csv")
    print("...Saved")

# CHecks if the Measurement Number is the same to all instruments (it's parralel process)
# And selects the minimum number
def Correct_Measurements_Number(instruments_info):
    instruments_num = len(instruments_info)
    measurement_size = int(instruments_info[0]['Measurement Number'])
    for i in range(0, instruments_num):
        if measurement_size <  int(instruments_info[i]['Measurement Number']):
            instruments_info[i]['Measurement Number'] = str(measurement_size)
    return instruments_info

def Task_0_array(instruments_info):
    time_step = 0.25
    instruments_setup_values = Setup_Values(instruments_info)
    instruments_info.pop(0)  # ------------------- remove the 1st element which contains the instruments_setup_values
    instruments_info = Correct_Measurements_Number(instruments_info) # selects the minimum number of measurements
    Print_Instruments_info(instruments_info)
    # ------------------- Here we Setup the instruments and ready execution
    sourcemeters = Setup_Instruments(instruments_setup_values, instruments_info)
    # print("Sourcemeter:",sourcemeters)
    # ------------------- Here we Start the measurements in parallel execution
    # return_values = Start_Instruments_Sequential(sourcemeters)
    return_values, timestamps = Start_Instruments_Parallel(sourcemeters, time_step) # is a list of tuples (applied_values, measured_values)
    # print("Returned Values:",return_values)
    Store_Data(return_values, instruments_info, time_step, timestamps)

    print("-----------\n")
    return "GOOD!"


def change_appearance_mode_event(new_appearance_mode: str):
    customtkinter.set_appearance_mode(new_appearance_mode)


def MouseWheelHandler(event):
    global count

    def delta(event):
        if event.num == 5 or event.delta < 0:
            return -1
        return 1

    count += delta(event)
    print(count)


def Sub_Plot(axis, subplot_x, sublplot_y, x_data, y_data, plot_title, plot_x_label, plot_y_label):
    axis[subplot_x, sublplot_y].plot(x_data, y_data)
    axis[subplot_x, sublplot_y].set_title(plot_title)
    axis[subplot_x, sublplot_y].set_xlabel(plot_x_label)
    axis[subplot_x, sublplot_y].set_ylabel(plot_y_label)


def graph(data_path):
    print("Data Path for Plotting:",data_path)
    df = pd.read_csv(data_path)
    df_column_names = list(df.columns)[1:]
    columns_num = len(df_column_names)
    instruments_num = int((len(df_column_names) - 1) / 2)
    print(df_column_names)
    print("Number of columns:", columns_num)
    print("Number of instruments:", instruments_num)
    fig, axs = plt.subplots(instruments_num, 3)
    column_pointer = 1
    column_border = 0
    for i in range(0, instruments_num):
        Sub_Plot(axis=axs,
                 subplot_x=2,
                 sublplot_y=i,
                 x_data=df[df_column_names[column_pointer]].values,
                 y_data=df[df_column_names[column_pointer + 1]].values,
                 plot_title=df_column_names[column_pointer][0:7],
                 plot_x_label=df_column_names[column_pointer][7:],
                 plot_y_label=df_column_names[column_pointer + 1][7:])
        Sub_Plot(axis=axs,
                 subplot_x=1,
                 sublplot_y=i,
                 x_data=df[df_column_names[0]].values,
                 y_data=df[df_column_names[column_pointer + 1]].values,
                 plot_title=df_column_names[column_pointer][0:7],
                 plot_x_label=df_column_names[0],
                 plot_y_label=df_column_names[column_pointer + 1][7:])
        Sub_Plot(axis=axs,
                 subplot_x=0,
                 sublplot_y=i,
                 x_data=df[df_column_names[0]].values,
                 y_data=df[df_column_names[column_pointer]].values,
                 plot_title=df_column_names[column_pointer][0:7],
                 plot_x_label=df_column_names[0],
                 plot_y_label=df_column_names[column_pointer][7:])
        rect = plt.Rectangle(
            # (lower-left corner), width, height
            (0.01 + column_border, 0.01), 0.30, 0.97, fill=False, color="k", lw=1,
            zorder=1000, transform=fig.transFigure, figure=fig
        )
        fig.patches.extend([rect])
        column_border += 0.334
        column_pointer += 2
    fig.tight_layout()
    plt.show()


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.instruments_search = "N/A"
        self.instruments_setup_values = {
            # ------------ for "Measure Current" Arguments
            "Voltage Range [Measure Current]": "None",  # value (in Volts) or None
            "Compliance Current [Measure Current]": "1011E-4",
            # A floating point property that controls the compliance current in Amps
            "Power Line Cycles [Measure Current]": "1",  # Number of power line cycles (NPLC) from 0.01 to 10
            "Current Range [Measure Current]": "0.000105",  # in Amps; Upper limit of current in Amps, from -1.05 A
            "Auto Range [Measure Current]": "True",  # Enables auto_range if True, else uses the set resistance
            # ------------ for "Measure Voltage" Arguments
            "Current Range [Measure Voltage]": "None",
            "Compliance Voltage [Measure Voltage]": "0.1",
            "Power Line Cycles [Measure Voltage]": "1",
            "Voltage Range [Measure Voltage]": "21.0",
            "Auto Range [Measure Voltage]": "True"
        }
        self.init_sidebar_value = "1"  # <--- The initial State (default Instrument Number displayed)
        self.repetition_num = "1"
        self.group_frame = None
        self.entry_button = None
        self.single_frame_form = None
        self.single_frame_option_menu = None
        self.single_frame_mode = None
        self.single_frame_title_text = None
        self.single_frame_title = None
        self.single_frame_title_val = None
        self.single_frame_label = None
        self.single_frame_data = None
        self.single_frame = None
        self.single_frame_entry = None
        self.filename = 'data/Results-06-04-2023-11:37:00.csv'
        self.anim = None
        self.line = None

        # -----------------------------------------------------Window---------------------------------------------------
        # configure window
        self.title("Instruments Operation Control")
        self.geometry(f"{1250}x{1150}")  # {width}x{height}
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)
        # --------------------------------------------------Side Bar----------------------------------------------------
        # Create sidebar Frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=100, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=5, columnspan=1, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        # Side Bar --> Title
        self.sidebar_title_label = customtkinter.CTkLabel(master=self.sidebar_frame, text="Operation Panel",
                                                          font=("Calibre", 16), anchor="nw")
        self.sidebar_title_label.grid(row=0, column=0, padx=20, pady=(10, 10))

        # Side Bar Frame --> Search Instruments ------------------------------------------------------------------------
        self.sidebar_instruments_search_frame = customtkinter.CTkFrame(master=self.sidebar_frame)
        self.sidebar_instruments_search_frame.grid(row=1, column=0, sticky="nsew", pady=(10, 10))
        # ------------- Side Bar > Search Instruments Frame ---> Label Title
        self.sidebar_search_instruments_label = customtkinter.CTkLabel(master=self.sidebar_instruments_search_frame,
                                                                       text="Available Instruments",
                                                                       anchor="w")
        self.sidebar_search_instruments_label.grid(row=0, column=0, padx=10, pady=(10, 0))
        # ------------- Side Bar > Search Instruments Frame ---> Button
        self.sidebar_search_instruments_button = customtkinter.CTkButton(self.sidebar_instruments_search_frame,
                                                                         width=70,
                                                                         command=self.search_instrument_event,
                                                                         text="Search")
        self.sidebar_search_instruments_button.grid(row=0, column=1, padx=1, pady=(10, 0))
        # ------------- Side Bar > Search Instruments Frame ---> Label Value
        self.sidebar_search_instruments_label_value = customtkinter.CTkLabel(self.sidebar_instruments_search_frame,
                                                                             text=self.instruments_search,
                                                                             anchor="nw")
        self.sidebar_search_instruments_label_value.grid(row=1, column=0, padx=20, pady=(10, 0))

        # Side Bar Frame --> Select Instruments ------------------------------------------------------------------------
        self.sidebar_instruments_select_frame = customtkinter.CTkFrame(master=self.sidebar_frame)
        self.sidebar_instruments_select_frame.grid(row=2, column=0, sticky="nsew")
        # ------------- Side Bar > Select Instruments Frame ---> Label Title
        self.sidebar_option_menu_label = customtkinter.CTkLabel(self.sidebar_instruments_select_frame,
                                                                text="Select the Number of Instruments \n you want to "
                                                                     "operate",
                                                                anchor="w")
        self.sidebar_option_menu_label.grid(row=0, column=0, padx=20, pady=(10, 0))
        # ------------- Side Bar > Select Instruments Frame ---> Option Menu
        gpib_option_menu_values = ["1", "2", "3", "4", "5", "6", "7"]
        self.sidebar_option_menu = customtkinter.CTkOptionMenu(self.sidebar_instruments_select_frame,
                                                               values=gpib_option_menu_values,
                                                               command=self.sidebar_option_menu_event)
        self.sidebar_option_menu.grid(row=1, column=0, padx=20, pady=(10, 10))
        self.sidebar_option_menu.set(self.init_sidebar_value)

        # Side Bar --> Appearance Mode (Extra Options)
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_option_menu = customtkinter.CTkOptionMenu(self.sidebar_frame,
                                                                       values=["Light", "Dark", "System"],
                                                                       command=change_appearance_mode_event)
        self.appearance_mode_option_menu.grid(row=8, column=0, padx=20, pady=(10, 10))
        self.appearance_mode_option_menu.set("Dark")
        # Side Bar --> Window Scale (Extra Options)
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=9, column=0, padx=20, pady=(10, 0))
        self.scaling_option_menu = customtkinter.CTkOptionMenu(self.sidebar_frame,
                                                               values=["80%", "90%", "100%", "110%", "120%", "130%"],
                                                               command=self.change_scaling_event)
        self.scaling_option_menu.set("100%")
        self.scaling_option_menu.grid(row=10, column=0, padx=20, pady=(10, 20))

        # --------------------------------------- Top Widget - Main Frame ----------------------------------------------
        # Create the Top Main Frame
        self.top_main_frame = customtkinter.CTkFrame(self, height=250, width=700, corner_radius=0)
        self.top_main_frame.grid(row=0, column=1, padx=(20, 20), pady=(20, 0), sticky="W")
        # Top Frame --> Labels Will be updated
        # Top Widget --> Instrument status ---------------------------------------------------------------
        self.status_label_frame = customtkinter.CTkFrame(self.top_main_frame, corner_radius=0)
        self.status_label_frame.grid(row=0, column=0, padx=(5, 20), pady=(20, 10), sticky="W")

        self.status_label_title = customtkinter.CTkLabel(self.status_label_frame,
                                                         text="Number of Instruments Selected:",
                                                         font=("Calibre", 18))
        self.status_label_title.grid(row=0, column=0, padx=5, pady=(10, 0), sticky="W")
        self.status_label_value = customtkinter.CTkLabel(self.status_label_frame, text=self.init_sidebar_value,
                                                         width=40,
                                                         corner_radius=5,
                                                         font=("Calibre", 18),
                                                         fg_color="#1F6AA5")
        self.status_label_value.grid(row=0, column=1, padx=(0, 20), pady=(10, 0), sticky="W")
        # Top Widget --> Default Values ---------------------------------------------------------------
        self.top_main_instrumentation = customtkinter.CTkFrame(self.top_main_frame,
                                                               # width=90,
                                                               fg_color="#333333",
                                                               corner_radius=10)
        self.top_main_instrumentation.grid(row=3, column=0, padx=(5, 5), pady=(5, 10), sticky="S")

        self.top_main_label_title = customtkinter.CTkLabel(self.top_main_instrumentation,
                                                           text="Insert Instrument's Setup Values:")
        self.top_main_label_title.grid(row=0, column=0, sticky=tkinter.W, pady=2, padx=(5, 5))

        curr_row_counter = 1
        self.instruments_tk_setup_values = []
        for curr_label, curr_entry in self.instruments_setup_values.items():
            self.top_main_label_inst = customtkinter.CTkLabel(self.top_main_instrumentation, text=curr_label)
            self.top_main_label_inst.grid(row=curr_row_counter, column=0, sticky=tkinter.W, pady=2, padx=(5, 5))
            self.top_main_entry_inst = customtkinter.CTkEntry(self.top_main_instrumentation,
                                                              corner_radius=0,
                                                              width=300)
            self.top_main_entry_inst.delete(0)
            self.top_main_entry_inst.insert(0, curr_entry)
            self.top_main_entry_inst.grid(row=curr_row_counter, column=1, pady=2, padx=(5, 5))
            self.instruments_tk_setup_values.append((self.top_main_label_inst, self.top_main_entry_inst))
            curr_row_counter = curr_row_counter + 1

        # --------------------------------------- Core Widget - Main Frame ---------------------------------------------
        # Create the Core Main Frame with widgets
        self.main_frame = customtkinter.CTkScrollableFrame(self, height=400, width=700, corner_radius=0)
        self.main_frame.grid(row=1, column=1, padx=(20, 20), pady=(20, 0), sticky="W")
        # Main Frame --> Generate Individual Frame Data for each GPIB
        # "group_data" refer to all the data which will be completed and will be sent to the GPIBs
        # "group_data_tk" refer to all the tk data relevant to the group_data which operate the UI
        self.group_data = []  # 3D-Array (1st: the individual frame; 2nd: the label; 3rd: the entry)
        self.group_data_tk = []
        self.generate_group_frame()

        # --------------------------------------------------Right Side Bar----------------------------------------------
        # Create RIGHT sidebar Frame with widgets
        self.right_sidebar_frame = customtkinter.CTkFrame(self, height=300, width=120, corner_radius=0)
        self.right_sidebar_frame.grid(row=0, column=2, sticky="NW")
        # Side Bar --> Title
        self.right_sidebar_title_label = customtkinter.CTkLabel(master=self.right_sidebar_frame, text="Plots Panel",
                                                                font=("Calibre", 16), anchor="n")
        self.right_sidebar_title_label.grid(row=0, column=0, padx=20, pady=(10, 10))

        self.plot_file_button = customtkinter.CTkButton(master=self.right_sidebar_frame,
                                                        text='Open a File',
                                                        command=self.select_file)
        self.plot_file_button.grid(row=1, column=0, pady=10, padx=20, sticky="w")
        self.plot_file_name_title = customtkinter.CTkLabel(master=self.right_sidebar_frame, text="File Selected:",
                                                           font=("Calibre", 15))
        self.plot_file_name_title.grid(row=2, column=0, padx=(5,0), pady=(10, 0), sticky="w")
        self.plot_file_name_label = customtkinter.CTkLabel(master=self.right_sidebar_frame, font=("Calibre", 12),
                                                           text="No File Selected")
        self.plot_file_name_label.grid(row=3, column=0, padx=(5,0), pady=(0,10), sticky="w")
        self.plot_button = customtkinter.CTkButton(master=self.right_sidebar_frame,
                                                   command= lambda: graph(self.filename),
                                                   text="Show Graph")
        self.plot_button.grid(row=4, column=0, pady=10, padx=20, sticky="w")



    # ----------------------------------This Generates the GPIB Group Frames--------------------------------------------
    def generate_group_frame(self):
        # Group Frame which includes GPIBs
        self.group_frame = customtkinter.CTkFrame(self.main_frame, width=120, corner_radius=0)
        self.group_frame.grid(row=2, column=2, padx=(20, 20), pady=(20, 20), sticky="W", columnspan=2)
        self.group_frame.grid_rowconfigure(1, weight=1)
        self.group_data_tk = []
        if len(self.group_data) == 0:  # <----- the initial state
            self.sidebar_option_menu_event(self.status_label_value.cget("text"))
        else:
            for i in range(0, int(self.status_label_value.cget("text"))):
                # Single Frame
                self.single_frame = customtkinter.CTkFrame(self.group_frame, width=190)
                self.single_frame.grid(row=i + 1, column=0, padx=(5, 5), pady=(5, 10), sticky="W")
                self.single_frame_data = self.group_data[i]
                self.group_data_tk.append(self.generate_single_frame)

        self.measure_button_frame = customtkinter.CTkFrame(self.group_frame)
        self.measure_button_frame.grid(row=1, column=1, padx=(20, 5), pady=(0, 5))

        self.entry_button = customtkinter.CTkButton(master=self.measure_button_frame, command=self.measure_event,
                                                    text="Start Measurement")
        self.entry_button.grid(row=0, column=0, pady=10, padx=20, sticky="n")
        self.entry_button_label = customtkinter.CTkLabel(self.measure_button_frame, font=("Calibre", 12),
                                                         text="Number of Repetitions")
        self.entry_button_label.grid(row=1, column=0, pady=0, padx=20, sticky="W")

        self.entry_button_entry = customtkinter.CTkEntry(self.measure_button_frame,
                                                         corner_radius=0,
                                                         width=50)
        self.entry_button_entry.delete(0)
        self.entry_button_entry.insert(0, self.repetition_num)
        self.entry_button_entry.grid(row=1, column=2, pady=0, padx=5, sticky="W")

    # ----------------------------------This Generates the GPIB Group Frames--------------------------------------------
    @property
    def generate_single_frame(self):
        single_frame_tuple = []
        # Generate Single Form --> Head
        self.single_frame_title = customtkinter.CTkFrame(self.single_frame)
        self.single_frame_title.grid(row=0, column=0, padx=(5, 5), pady=(5, 5))
        self.single_frame_title_text = customtkinter.CTkLabel(self.single_frame_title, font=("Calibre", 16),
                                                              text="Instrument ")
        self.single_frame_title_text.grid(row=0, column=0, padx=(5, 1))
        self.single_frame_title_val = customtkinter.CTkLabel(self.single_frame_title, font=("Calibre", 16),
                                                             text=self.single_frame_data.get("Instrument"))
        self.single_frame_title_val.grid(row=0, column=1, padx=(1, 5))
        single_frame_tuple.append(("Instrument", self.single_frame_title_val))

        # Generate Single Form --> Option Menu
        self.single_frame_mode = customtkinter.CTkFrame(self.single_frame, width=120)
        self.single_frame_mode.grid(row=1, column=0, padx=(5, 5), pady=(0, 5))
        single_frame_mode_values = ["Apply Incremental Voltage",
                                    "Apply Steady Voltage",
                                    "Apply Incremental Current",
                                    "Apply Steady Current"
                                    ]
        self.single_frame_option_menu = customtkinter.CTkOptionMenu(self.single_frame_mode,
                                                                    values=single_frame_mode_values,
                                                                    command=self.single_frame_mode_event)
        self.single_frame_option_menu.set(self.single_frame_data.get("OptionMenu"))
        self.single_frame_option_menu.grid(row=0, column=0, padx=20, pady=(5, 5))
        single_frame_tuple.append(("OptionMenu", self.single_frame_option_menu))
        # Generate the Single Form --> Labels & Entries
        # Form Line "row_counter" --> Label Will be updated ("row_counter")
        self.single_frame_form = customtkinter.CTkFrame(self.single_frame, width=120, corner_radius=0)
        self.single_frame_form.grid(row=2, column=0)
        row_counter = 0
        for label, entry in self.single_frame_data.items():
            if label != "Instrument" and label != "OptionMenu":
                self.single_frame_label = customtkinter.CTkLabel(self.single_frame_form, text=label)
                self.single_frame_label.grid(row=row_counter, column=0, sticky=tkinter.W, pady=2, padx=(5, 5))
                self.single_frame_entry = customtkinter.CTkEntry(self.single_frame_form,
                                                                 corner_radius=0,
                                                                 width=150)
                self.single_frame_entry.delete(0)
                self.single_frame_entry.insert(0, entry)
                self.single_frame_entry.grid(row=row_counter, column=1, pady=2, padx=(5, 5))
                single_frame_tuple.append((self.single_frame_label, self.single_frame_entry))
                row_counter += 1
        return single_frame_tuple

    # ------------------------------- This Updates the Number of GPIB Frames--------------------------------------------
    def sidebar_option_menu_event(self, new_appearance_mode: str):
        self.status_label_value.configure(text=new_appearance_mode)
        print("Status:", self.status_label_value.cget("text"))
        # ---------------- Generate frames relative to the inserted GPIB number
        self.group_data = []
        for i in range(0, int(self.status_label_value.cget("text"))):
            self.group_data.append({
                "Instrument": str(i + 1),
                "OptionMenu": "Apply Incremental Voltage",
                "Port Number": "GPIB::" + str(i),
                "Measurement Number": str(10 + i),
                "Min Voltage (Volts)": str(i),
                "Max Voltage (Volts)": str(i + 10)
            })
        self.group_frame.destroy()
        self.generate_group_frame()

    # ------------------------------- This Updates the Single GPIB Operation--------------------------------------------
    def single_frame_mode_event(self, single_frame_mode: str):
        # -------------------------------------------------------------------------------------------------------------------------
        updated_group_data = []
        # ---------- Generate the new data based on the Intput from TK
        for single_group_data_tk in self.group_data_tk:
            single_group_data = dict(Instrument=single_group_data_tk[0][1].cget("text"),
                                     OptionMenu=single_group_data_tk[1][1].get())
            for i in range(2, len(single_group_data_tk)):
                single_group_data[str(single_group_data_tk[i][0].cget("text"))] = str(single_group_data_tk[i][1].get())
            updated_group_data.append(single_group_data)

        new_group_data = []
        for i in range(len(self.group_data)):
            print("Instrument: ", i + 1)
            previous_single_data = self.group_data[i]
            updated_single_data = updated_group_data[i]
            if previous_single_data["OptionMenu"] != updated_single_data["OptionMenu"]:
                print("CHANGED")
                if updated_single_data["OptionMenu"] == "Apply Steady Voltage":
                    new_single_group_data = {
                        "Instrument": previous_single_data["Instrument"],
                        "OptionMenu": updated_single_data["OptionMenu"],
                        "Port Number": updated_single_data["Port Number"],
                        "Measurement Number": updated_single_data["Measurement Number"],
                        "Steady Voltage (Volts)": str(10),
                    }
                if updated_single_data["OptionMenu"] == "Apply Incremental Voltage":
                    new_single_group_data = {
                        "Instrument": previous_single_data["Instrument"],
                        "OptionMenu": updated_single_data["OptionMenu"],
                        "Port Number": updated_single_data["Port Number"],
                        "Measurement Number": updated_single_data["MMeasurement Number"],
                        "Min Voltage (Volts)": str(1),
                        "Max Voltage (Volts)": str(10)
                    }
                if updated_single_data["OptionMenu"] == "Apply Steady Current":
                    new_single_group_data = {
                        "Instrument": previous_single_data["Instrument"],
                        "OptionMenu": updated_single_data["OptionMenu"],
                        "Port Number": updated_single_data["Port Number"],
                        "Measurement Number": updated_single_data["Measurement Number"],
                        "Steady Current (Amps)": str(10),
                    }
                if updated_single_data["OptionMenu"] == "Apply Incremental Current":
                    new_single_group_data = {
                        "Instrument": previous_single_data["Instrument"],
                        "OptionMenu": updated_single_data["OptionMenu"],
                        "Port Number": updated_single_data["Port Number"],
                        "Measurement Number": updated_single_data["Measurement Number"],
                        "Min Current (Amps)": str(1),
                        "Max Current (Amps)": str(10)
                    }
                new_group_data.append(new_single_group_data)
            else:  # <-------- if there is no change at the OptionMenu we keep it the same (previous)
                new_group_data.append(previous_single_data)

            # print("Before:", previous_single_data)
            print("   New:", new_group_data)
        self.group_data = new_group_data
        # -------------------------------------------------------------------------------------------------------------------------
        self.group_frame.destroy()
        self.generate_group_frame()

    def update_instruments_setup_values_event(self):
        # ---------- Take the new Instrument data from Top Main Frame from TK
        updated_instruments_setup_values = {}
        for single_setup_value in self.instruments_tk_setup_values:
            single_setup_value_label = single_setup_value[0].cget("text")
            single_setup_value_value = single_setup_value[1].get()
            # print(single_setup_value_label,single_setup_value_value)
            updated_instruments_setup_values[single_setup_value_label] = single_setup_value_value
        return updated_instruments_setup_values

    def update_instruments_functional_values_event(self):
        updated_group_data = []
        # ---------- Generate the new data based on the Intput from TK
        for single_group_data_tk in self.group_data_tk:
            single_group_data = dict(Instrument=single_group_data_tk[0][1].cget("text"),
                                     OptionMenu=single_group_data_tk[1][1].get())
            for i in range(2, len(single_group_data_tk)):
                single_group_data[str(single_group_data_tk[i][0].cget("text"))] = str(single_group_data_tk[i][1].get())
            updated_group_data.append(single_group_data)
        return updated_group_data

    def measure_event(self):
        self.repetition_num = self.entry_button_entry.get()
        # print("Repetition Number:", self.repetition_num )
        self.group_data = self.update_instruments_functional_values_event()
        # print(self.group_data)


        self.openNewWindow()
        return None


        self.instruments_setup_values = self.update_instruments_setup_values_event()
        for rep in range(0, int(self.repetition_num)):
            print("Repetition:", rep + 1)
            task_result = Task_0_array([self.instruments_setup_values] + self.group_data)
            # <--- a list of dictionaries, each dictornery is an instrument
            print(task_result)

    def animate(self, i):
        x = np.linspace(0, 2, 1000)
        y = np.sin(2 * np.pi * (x - 0.01 * i))
        self.line.set_data(x, y)
        return self.line,

    def openNewWindow(self):
        print("test")
        # Toplevel object which will be treated as a new window
        self.newWindow = customtkinter.CTkToplevel(self)
        # sets the title of the
        # Toplevel widget
        self.newWindow.title("New Window")
        # sets the geometry of toplevel
        self.newWindow.geometry("200x200")
        # A Label widget to show in toplevel
        customtkinter.CTkLabel(master=self.newWindow, text="This is a new window")

        fig = plt.Figure(dpi=100)
        ax = fig.add_subplot(xlim=(0, 2), ylim=(-1, 1))
        self.line, = ax.plot([], [], lw=2)
        canvas = FigureCanvasTkAgg(fig, master=self.newWindow)
        canvas.get_tk_widget().pack(side=customtkinter.TOP, fill=customtkinter.BOTH, expand=1)

        self.anim = animation.FuncAnimation(fig, self.animate, frames=1000, interval=100, blit=True)


    def search_instrument_event(self):
        get_connected_instuments = Get_Connected_Instruments()
        delimiter_value = "\n"  # initializing delimiter
        res = ''
        for ele in get_connected_instuments:  # using loop to add string followed by delim
            res = res + str(ele) + delimiter_value
        self.sidebar_search_instruments_label_value.configure(text=res)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def select_file(self):
        filetypes = (('text files', '*.csv'), ('All files', '*.*'))
        self.filename = fd.askopenfilename(title='Open a file', filetypes=filetypes)
        print(self.filename)
        self.plot_file_name_label.configure(text=self.filename[-23:])


if __name__ == "__main__":
    app = App()
    count = 0
    app.bind("<MouseWheel>", MouseWheelHandler)
    app.bind("<Button-4>", MouseWheelHandler)
    app.bind("<Button-5>", MouseWheelHandler)
    app.mainloop()
