# Import the required Libraries
from tkinter import *
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt

# Create an instance of Tkinter frame
win = Tk()

# Set the geometry of tkinter frame
win.geometry("750x250")


def Sub_Plot(axis, subplot_x, sublplot_y, x_data, y_data, plot_title, plot_x_label, plot_y_label):
    axis[subplot_x, sublplot_y].plot(x_data, y_data)
    axis[subplot_x, sublplot_y].set_title(plot_title)
    axis[subplot_x, sublplot_y].set_xlabel(plot_x_label)
    axis[subplot_x, sublplot_y].set_ylabel(plot_y_label)


def graph():
    df = pd.read_csv('data.csv')
    df_column_names = list(df.columns)[1:]
    columns_num = len(df_column_names)
    instruments_num = int((len(df_column_names) - 1) / 2)
    print(df_column_names)
    print("Number of columns:", columns_num)
    print("Number of instruments:", instruments_num)
    fig, axs = plt.subplots(instruments_num, 3)
    column_pointer = 1
    for i in range(0, instruments_num):
        Sub_Plot(axis=axs,
                 subplot_x=i,
                 sublplot_y=0,
                 x_data=df[df_column_names[column_pointer]].values,
                 y_data=df[df_column_names[column_pointer + 1]].values,
                 plot_title=df_column_names[column_pointer][0:7],
                 plot_x_label=df_column_names[column_pointer][7:],
                 plot_y_label=df_column_names[column_pointer + 1][7:])
        Sub_Plot(axis=axs,
                 subplot_x=i,
                 sublplot_y=1,
                 x_data=df[df_column_names[0]].values,
                 y_data=df[df_column_names[column_pointer]].values,
                 plot_title=df_column_names[column_pointer][0:7],
                 plot_x_label=df_column_names[0],
                 plot_y_label=df_column_names[column_pointer][7:])
        Sub_Plot(axis=axs,
                 subplot_x=i,
                 sublplot_y=2,
                 x_data=df[df_column_names[0]].values,
                 y_data=df[df_column_names[column_pointer + 1]].values,
                 plot_title=df_column_names[column_pointer][0:7],
                 plot_x_label=df_column_names[0],
                 plot_y_label=df_column_names[column_pointer + 1][7:])
        column_pointer += 2
    fig.tight_layout()
    plt.show()


# Create a button to show the plot
Button(win, text="Show Graph", command=graph).pack(pady=20)
win.mainloop()
