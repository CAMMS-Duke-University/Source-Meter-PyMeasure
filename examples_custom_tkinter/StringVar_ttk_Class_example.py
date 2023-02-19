import tkinter as tk
from tkinter import ttk

class User_Input(tk.Tk):
    def __init__(self):
        super().__init__()
        self.message = tk.StringVar(value="Nothing selected!")
        options = ["Option A", "Option B"]
        ttk.OptionMenu(self, tk.StringVar(),
                       "Select an option", *options,
                       command=lambda x: self.optionsCallback(x, "A")).pack()

        ttk.OptionMenu(self, tk.StringVar(),
                       "Select an option", *options,
                       command=lambda x: self.optionsCallback(x, "B")).pack()

        ttk.Label(self, textvariable=self.message).pack()

    def optionsCallback(self, selection, menu):
        if menu == 'A':
            self.message.set("this is menu A, " + selection)
        if menu == 'B':
            self.message.set("this is menu B, " + selection)



if __name__ == "__main__":
    app = User_Input()
    app.mainloop()
