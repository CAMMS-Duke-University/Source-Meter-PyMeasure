import tkinter as tk


class MyGUI:
    def __init__ (self):

        self.root = tk.Tk()
        self.root.geometry("1500x600")
        self.root.title("Keithley Console")

        self.label = tk.Label(self.root, text="Insert the Keithley2400 Parameters", font=('Arial', 16))
        self.label.pack(padx=50, pady=20)

        self.myentry = tk.Entry(self.root)
        self.myentry.pack()

        self.button = tk.Button(self.root, text="Start Measure", font=('Arial', 16), command=self.start_keithley)
        self.button.pack(padx=50, pady=20)

        self.root.mainloop()

    def start_keithley(self):
        print("Keithley Starts..")
        entry_string = self.myentry.get()
        print(entry_string)
        self.label.configure(text=entry_string)

MyGUI()
