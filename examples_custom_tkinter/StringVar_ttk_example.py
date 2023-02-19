import tkinter as tk
from tkinter import ttk

root = tk.Tk()
message = tk.StringVar(value="Nothing selected!")
options = ["Option A", "Option B"]

def optionsCallback(selection, menu):
    if menu == 'A':
        message.set("this is menu A, " + selection)
    if menu == 'B':
        message.set("this is menu B, " + selection)

ttk.OptionMenu(root, tk.StringVar(),
               "Select an option", *options,
               command=lambda x: optionsCallback(x, "A")).pack()

ttk.OptionMenu(root, tk.StringVar(),
               "Select an option", *options,
               command=lambda x: optionsCallback(x, "B")).pack()

ttk.Label(root, textvariable=message).pack()

root.mainloop()