import tkinter
import tkinter.messagebox
import customtkinter

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"



def makeform(self_frame, label_fields):
    entries = []
    for i in range(0, len(label_fields)):
        field = label_fields[i]
        # Text Frame
        text_frame_list_item = customtkinter.CTkFrame(self_frame)
        text_frame_list_item.grid(row=i+1, column=1)
        # Label Will be updated
        status_label_list = customtkinter.CTkLabel(text_frame_list_item, text=field)
        status_label_list.grid()
        entries.append(status_label_list)
    return entries

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("CustomTkinter complex_example.py")
        self.geometry(f"{600}x{480}")

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

        # Title Text Frame
        self.text_frame = customtkinter.CTkFrame(self, width=40, corner_radius=0)
        self.text_frame.grid(row=0, column=1, rowspan=1, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.text_frame.grid_rowconfigure(4, weight=1)
        # Label Will be updated
        self.status_label_title = customtkinter.CTkLabel(self.text_frame, text="Incremental Factor: ")
        self.status_label_title.grid(row=0, column=0, padx=20, pady=(10, 0))
        self.status_label = customtkinter.CTkLabel(self.text_frame, text="+0")
        self.status_label.grid(row=0, column=1, pady=(10, 0))

        # Label List Frame
        self.text_frame_list = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.text_frame_list.grid(row=1, column=1, padx=(20, 20), pady=(20, 0), sticky="nsew")
        label_values = ["0","1","2","3","4","5"]
        self.ents = makeform(self.text_frame_list, label_values)

    def mode_event(self, new_appearance_mode: str):
        print("Pointer:",self.status_label)
        current_value_string = self.status_label.cget("text")
        print("Current Value:",current_value_string)
        self.status_label.configure(text=new_appearance_mode)
        new_value_string = self.status_label.cget("text")
        print("New Value:",new_value_string)
        for ent in self.ents:
            update_label(ent,new_appearance_mode)

def update_label(self_label, new_value):
    current_value_string = self_label.cget("text")
    current_value = int(current_value_string)
    inc_factor = int(new_value[1])
    new_value = current_value + inc_factor
    self_label.configure(text=str(new_value))


if __name__ == "__main__":
    app = App()
    app.mainloop()