# TEST FUNCTION --> INSERT ENTRIES BASED ON fields length
#                   WITH DEFAULT ENTRY values
#                   PRINTS ON TERMINAL THE ENTRY VALUES

import examples_custom_tkinter as tk

def fetch(entries):
    for entry in entries:
        field = entry[0]
        text  = entry[1].get()
        print('%s: "%s"' % (field, text))

def makeform(root, label_fields, entry_fields):
    entries = []
    for i in range(0,len(label_fields)):
        field = label_fields[i]
        ent_default = entry_fields[i]
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

    number_of_GPIBs = 5
    label_fields = ['Label '+str(x) for x in range(1,number_of_GPIBs+1)]
    entry_fields = ['Entry '+str(x) for x in range(1,number_of_GPIBs+1)]

    ents = makeform(root, label_fields, entry_fields)
    root.bind('<Return>', (lambda event, e=ents: fetch(e)))

    b1 = tk.Button(root, text='Show', command=(lambda e=ents: fetch(e)))
    b1.pack(side=tk.LEFT, padx=5, pady=5)


    root.mainloop()
