# TEST FUNCTION --> JUST INSERT 2 ENTRIES NO ACTION

from tkinter import *

class LabeledEntry(Frame):
    def __init__(self, parent, *args, **kargs):
        text = kargs.pop("text")
        Frame.__init__(self, parent)
        Label(self, text=text, justify=LEFT).grid(sticky = W, column=0,row=0)
        Entry(self, *args, **kargs).grid(sticky = E, column=1, row=0)

class User_Input:
    def __init__(self, parent):
        fields = ['Text Label 1', 'Text Label 2',]
        GUIFrame =Frame(parent)
        GUIFrame.pack(expand=True, anchor=NW)
        parent.minsize(width=350, height=425)
        field_index = 1
        for field in fields:
            self.field = LabeledEntry(GUIFrame, text=field)
            self.field.grid(column=0, row=field_index)
            self.field.grid_columnconfigure(index = 0, minsize = 150)
            field_index += 1
        self.Button2 = Button(parent, text='exit', command= parent.quit)
        self.Button2.place(x=25, y=300)

root = Tk()

MainFrame =User_Input(root)
root.mainloop()
