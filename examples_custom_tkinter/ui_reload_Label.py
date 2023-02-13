import tkinter
import tkinter.messagebox
import customtkinter

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("CustomTkinter complex_example.py")
        self.geometry(f"{900}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        # Label Title
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Select Incremental Factor:", anchor="w")
        self.appearance_mode_label.grid(row=0, column=0, padx=20, pady=(10, 0))
        # Option Menu Title
        menu_values = ["+0","+1", "+2", "+3","+4","+5","+6","+7"]
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=menu_values,command=self.mode_event)
        self.appearance_mode_optionemenu.grid(row=1, column=0, padx=20, pady=(10, 10))

        # Text Frame
        self.text_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.text_frame.grid(row=0, column=1, rowspan=4, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.text_frame.grid_rowconfigure(4, weight=1)
        # Label Will be updated
        self.status_label = customtkinter.CTkLabel(self.text_frame, text="__")
        self.status_label.grid(row=2, column=0, padx=20, pady=(10, 0))


    def mode_event(self, new_appearance_mode: str):
        print(new_appearance_mode)
        print(type(new_appearance_mode))
        print("Pointer:",self.status_label)
        current_value_string = self.status_label.cget("text")
        print("Current Value:",current_value_string)
        self.status_label.configure(text=new_appearance_mode)
        new_value_string = self.status_label.cget("text")
        print("New Value:",new_value_string)




if __name__ == "__main__":
    app = App()
    app.mainloop()