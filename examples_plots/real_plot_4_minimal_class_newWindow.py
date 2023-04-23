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

    def openNewWindow(self):
        print("test")
        # Toplevel object which will be treated as a new window
        self.newWindow = tkinter.Toplevel(self)
        # sets the title of the
        # Toplevel widget
        self.newWindow.title("New Window")
        # sets the geometry of toplevel
        self.newWindow.geometry("200x200")
        # A Label widget to show in toplevel
        tkinter.Label(master=self.newWindow, text="This is a new window")

        fig = plt.Figure(dpi=100)
        ax = fig.add_subplot(xlim=(0, 2), ylim=(-1, 1))
        self.line, = ax.plot([], [], lw=2)
        canvas = FigureCanvasTkAgg(fig, master=self.newWindow)
        canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

        self.anim = animation.FuncAnimation(fig, self.animate, frames=1000, interval=100, blit=True)



    def __init__(self):
        super().__init__()

        self.anim = None
        self.line = None
        self.btn = tkinter.Button(master=self, text="New window", command=self.openNewWindow)
        self.btn.pack(pady=10)


if __name__ == "__main__":
    root = App()
    root.mainloop()
