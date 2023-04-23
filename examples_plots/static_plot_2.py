# Import the required Libraries
from tkinter import *
import numpy as np
import matplotlib.pyplot as plt

# Create an instance of Tkinter frame
win = Tk()

# Set the geometry of tkinter frame
win.geometry("750x250")


def graph():
    car_prices = np.random.normal(100000, 5000, 1000)
    plt.hist(car_prices, 20)
    plt.show()


# Create a button to show the plot
Button(win, text="Show Graph", command=graph).pack(pady=20)
win.mainloop()
