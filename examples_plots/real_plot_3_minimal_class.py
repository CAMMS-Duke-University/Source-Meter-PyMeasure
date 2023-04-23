import tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import pyplot as plt, animation
import numpy as np


class App(tkinter.Tk):

    def animate(self, i):
        x = np.linspace(0, 2, 1000)
        y = np.sin(2 * np.pi * (x - 0.01 * i))
        self.line.set_data(x, y)
        return self.line,

    def __init__(self):
        super().__init__()
        self.fig = plt.Figure(dpi=100)
        self.ax = self.fig.add_subplot(xlim=(0, 2), ylim=(-1, 1))
        self.line, = self.ax.plot([], [], lw=2)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

        self.anim = animation.FuncAnimation(self.fig, self.animate, frames=1000, interval=100, blit=True)


if __name__ == "__main__":
    root = App()
    root.mainloop()
