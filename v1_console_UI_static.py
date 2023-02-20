from keithley_functions import * # importing  all the Keithley libs
#import examples_custom_tkinter as tk
import tkinter as tk
import pandas as pd

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
        row = tk.Frame(root)
        lab = tk.Label(row, width=15, text = field, anchor='w')
        ent = tk.Entry(row)
        ent.insert(0,ent_default)
        row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        lab.pack(side=tk.LEFT)
        ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
        entries.append((field, ent))
    return entries

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("1500x600")
    root.title("Keithley Console")

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
    ents = makeform(root, label_fields, entry_fields)
    root.bind('<Return>', (lambda event, e=ents: fetch(e)))

    b1 = tk.Button(root, text='Show', command=(lambda e=ents: fetch(e)))
    b1.pack(side=tk.LEFT, padx=5, pady=5)


    root.mainloop()
