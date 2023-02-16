import time
import tkinter
import tkinter.messagebox
import customtkinter

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

def makeform(self_frame, label_fields, entries_fields):
    fields = []
    for i in range(0, len(label_fields)):
        field = label_fields[i]
        entry = entries_fields[i]
        # Text Frame
        text_frame_list_item = customtkinter.CTkFrame(self_frame)
        text_frame_list_item.grid(row=i+1, column=1)
        # Label Will be updated
        status_label_list_item = customtkinter.CTkLabel(text_frame_list_item, text=field)
        status_label_list_item.grid()
        status_entry_list_item = customtkinter.CTkEntry(text_frame_list_item)
        status_entry_list_item.delete(0)
        status_entry_list_item.insert(0,entry)
        status_entry_list_item.grid()
        fields.append((status_label_list_item,status_entry_list_item))
    return fields

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

        # create checkbox and switch frame
        self.checkbox_slider_frame = customtkinter.CTkFrame(self)
        self.checkbox_slider_frame.grid(row=0, column=1, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.checkbox_1 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame)
        self.checkbox_1.grid(row=1, column=0, pady=(20, 0), padx=20, sticky="n")
        self.checkbox_2 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame)
        self.checkbox_2.grid(row=2, column=0, pady=(20, 0), padx=20, sticky="n")
        self.checkbox_3 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame)
        self.checkbox_3.grid(row=3, column=0, pady=20, padx=20, sticky="n")
        self.enty_button = customtkinter.CTkButton(master=self.checkbox_slider_frame, command=self.update_checkbox)
        self.enty_button.grid(row=4, column=0, pady=10, padx=20, sticky="n")


    def update_checkbox(self):
        cb_val_1 = self.checkbox_1.get()
        cb_val_2 = self.checkbox_2.get()
        cb_val_3 = self.checkbox_3.get()
        print(cb_val_1,cb_val_2,cb_val_3)

if __name__ == "__main__":
    app = App()
    app.mainloop()