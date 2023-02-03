import tkinter as tk


class MyGUI:
    def __init__ (self):
        fields = ['Text Label 1', 'Text Label 2']

        self.root = tk.Tk()
        self.root.geometry("1500x600")
        self.root.title("Keithley Console")

        row_num = 0
        # this will create a label widget
        self.label_1 = tk.Label(self.root, text="Label 1", font=('Arial', 16))
        # grid method to arrange label respective to row number
        self.label_1.grid(row = row_num, column = 0, sticky = tk.W, pady = 2)
        # entry widgets, used to take the entry
        self.entry_1 = tk.Entry(self.root)
        # this will arrange entry widget respective to row number
        self.entry_1.grid(row = row_num, column = 1, pady = 2)


        row_num = 1
        # this will create a label widget
        self.label_2 = tk.Label(self.root, text="Label 2", font=('Arial', 16))
        # grid method to arrange label respective to row number
        self.label_2.grid(row = row_num, column = 0, sticky = tk.W, pady = 2)
        # entry widgets, used to take the entry
        self.entry_2 = tk.Entry(self.root)
        # this will arrange entry widget respective to row number
        self.entry_2.grid(row = row_num, column = 1, pady = 2)


        self.root.mainloop()

MyGUI()
