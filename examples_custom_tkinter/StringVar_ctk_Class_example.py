import customtkinter


class User_Input(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.message = customtkinter.StringVar(value="Nothing selected!")
        options = ["Option A", "Option B"]
        customtkinter.CTkOptionMenu(self,
                                    variable=customtkinter.StringVar(),
                                    values=options,
                                    command=lambda x: self.optionsCallback(x, "A")).pack()

        customtkinter.CTkOptionMenu(self,
                                    variable=customtkinter.StringVar(),
                                    values=options,
                                    command=lambda x: self.optionsCallback(x, "B")).pack()

        customtkinter.CTkLabel(self, textvariable=self.message).pack()

    def optionsCallback(self, selection, menu):
        if menu == 'A':
            self.message.set("this is menu A, " + selection)
        if menu == 'B':
            self.message.set("this is menu B, " + selection)


if __name__ == "__main__":
    app = User_Input()
    app.mainloop()
