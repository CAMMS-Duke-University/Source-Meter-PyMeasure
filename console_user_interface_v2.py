from keithley_functions import * # importing  all the Keithley libs
import tkinter as tk
import customtkinter as ctk
import pandas as pd

    #number_of_entries = 5
    #label_fields = ['Label '+str(x) for x in range(1,number_of_entries+1)]
    #entry_fields = ['Entry '+str(x) for x in range(1,number_of_entries+1)]
label_fields = ['Instrument A Name',
                'Instrument B Name',
                'Voltage Range',
                'Compliance Current',
                'Number of Power Line Cycles',
                'Current Range',
                'Auto Range',
                'Number Measurements',
                'DC Voltage',
                'AC Min. Voltage',
                'AC Max. Voltage']
entry_fields = [
                "GPIB::3",
                "GPIB::6",
                None,
                10e-4,
                1,
                0.000105,
                True,
                10,
                1,
                1,
                10]

def fetch(entries):
    entry_values =[]
    for entry in entries:
        field = entry[0]
        value  = entry[1].get()
        entry_values.append(value)
        print('%s: "%s"' % (field, value))
    print("------")
    currents_A, currents_B = Task_1_array(entry_values)
    #currents_A, currents_B = Task_1 (entry_values)
    print(currents_A, currents_B)
    pd.DataFrame(currents_A).to_csv("Currents_A.csv")
    pd.DataFrame(currents_B).to_csv("Currents_B.csv")
    print("...Saved")

def makeform(root, label_fields, entry_fields):
    entries = []
    for i in range(0,len(label_fields)):
        field = label_fields[i]
        ent_default = str(entry_fields[i])
        row = ctk.CTkFrame(root)
        lab = ctk.CTkLabel(master=row, padx=5, height=35, corner_radius=8, text=field, anchor='w')
        ent = ctk.CTkEntry(master=row)
        ent.insert(0,ent_default)
        row.pack(side=ctk.TOP, fill=ctk.X, padx=100, pady=6)
        lab.pack(side=ctk.LEFT)
        ent.pack(side=ctk.RIGHT, expand=ctk.YES, fill=ctk.X)
        entries.append((field, ent))
    return entries

if __name__ == '__main__':

    ctk.set_appearance_mode("dark")  # Modes: system (default), light, dark
    ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

    root = ctk.CTk()
    root.geometry("1100x700")
    root.title("Keithley Console")

    label_head = ctk.CTkLabel(master=root, text="Current Measurement", justify=ctk.LEFT)
    label_head.pack(pady=10, padx=10)

    ents = makeform(root, label_fields, entry_fields)
    root.bind('<Return>', (lambda event, e=ents: fetch(e)))

    b1 = ctk.CTkButton(root, text='Show', command=(lambda e=ents: fetch(e)))
    b1.pack(side=ctk.LEFT, padx=10, pady=10)


    root.mainloop()
