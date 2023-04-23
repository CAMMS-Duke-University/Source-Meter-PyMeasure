import tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import pyplot as plt, animation
import numpy as np


def animate(i):
    x = np.linspace(0, 2, 1000)
    y = np.sin(2 * np.pi * (x - 0.01 * i))
    line.set_data(x, y)
    return line,


root = tkinter.Tk()

fig = plt.Figure(dpi=100)
ax = fig.add_subplot(xlim=(0, 2), ylim=(-1, 1))
line, = ax.plot([], [], lw=2)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

anim = animation.FuncAnimation(fig, animate, frames=1000, interval=100, blit=True)
root.mainloop()
