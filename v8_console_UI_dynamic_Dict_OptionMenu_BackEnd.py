from keithley_functions import * # importing  all the Keithley libs
import tkinter
import tkinter.messagebox
import customtkinter


customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


def change_appearance_mode_event(new_appearance_mode: str):
    customtkinter.set_appearance_mode(new_appearance_mode)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.init_sidebar_value = "1"  # <---------------------------- what is the initial State
        self.group_frame = None
        self.entry_button = None
        self.single_frame_form = None
        self.single_frame_option_menu = None
        self.single_frame_mode = None
        self.single_frame_title_text = None
        self.single_frame_title = None
        self.single_frame_title_val = None
        self.single_frame_label = None
        self.single_frame_data = None
        self.single_frame = None
        self.single_frame_entry = None
        # -----------------------------------------------------Window---------------------------------------------------
        # configure window
        self.title("Instruments Operation Control")
        self.geometry(f"{900}x{780}")
        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        # --------------------------------------------------Side Bar----------------------------------------------------
        # Create sidebar Frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        # Side Bar --> Label
        self.sidebar_option_menu_label = customtkinter.CTkLabel(self.sidebar_frame, text="Select Number of GPIBs:",
                                                                anchor="w")
        self.sidebar_option_menu_label.grid(row=0, column=0, padx=20, pady=(10, 0))
        # Side Bar --> Option Menu
        gpib_option_menu_values = ["1", "2", "3", "4", "5", "6", "7"]
        self.sidebar_option_menu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=gpib_option_menu_values,
                                                               command=self.sidebar_option_menu_event)
        self.sidebar_option_menu.grid(row=1, column=0, padx=20, pady=(10, 10))
        self.sidebar_option_menu.set(self.init_sidebar_value)
        # Side Bar --> Appearance Mode
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_option_menu = customtkinter.CTkOptionMenu(self.sidebar_frame,
                                                                       values=["Light", "Dark", "System"],
                                                                       command=change_appearance_mode_event)
        self.appearance_mode_option_menu.grid(row=6, column=0, padx=20, pady=(10, 10))
        # Side Bar --> Window Scale
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_option_menu = customtkinter.CTkOptionMenu(self.sidebar_frame,
                                                               values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_option_menu.set("100%")
        self.scaling_option_menu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # ------------------------------------------------Main Frame----------------------------------------------------
        # Create Main Frame with widgets
        self.main_frame = customtkinter.CTkScrollableFrame(self, width=180, height=400, corner_radius=0)
        self.main_frame.grid(row=0, column=1, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.main_frame.grid_rowconfigure(4, weight=1)
        # Main Frame --> Labels Will be updated
        self.status_label_title = customtkinter.CTkLabel(self.main_frame, text="Number of GPIBs:", font=("Calibre", 18))
        self.status_label_title.grid(row=0, column=0, padx=5, pady=(10, 0))
        self.status_label_value = customtkinter.CTkLabel(self.main_frame, text=self.init_sidebar_value,
                                                         font=("Calibre", 18))
        self.status_label_value.grid(row=0, column=1, pady=(10, 0))

        # Main Frame --> Generate Individual Frame Data for each GPIB
        # "group_data" refer to all the data which will be completed and will be sent to the GPIBs
        # "group_data_tk" refer to all the tk data relevant to the group_data which operate the UI
        self.group_data = []  # 3D-Array (1st: the individual frame; 2nd: the label; 3rd: the entry)
        self.group_data_tk = []
        self.generate_group_frame()

    # ----------------------------------This Generates the GPIB Group Frames--------------------------------------------
    def generate_group_frame(self):
        # Group Frame which includes GPIBs
        self.group_frame = customtkinter.CTkFrame(self.main_frame, width=160, corner_radius=0)
        self.group_frame.grid(row=2, column=2, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.group_frame.grid_rowconfigure(1, weight=1)
        self.group_data_tk = []
        if len(self.group_data) == 0:  # <----- the initial state
            self.sidebar_option_menu_event(self.status_label_value.cget("text"))
        else:
            for i in range(0, int(self.status_label_value.cget("text"))):
                # Single Frame
                self.single_frame = customtkinter.CTkFrame(self.group_frame, width=190)
                self.single_frame.grid(row=i + 1, column=1, padx=(5, 5), pady=(5, 10), sticky="nsew")
                self.single_frame_data = self.group_data[i]
                self.group_data_tk.append(self.generate_single_frame)
        self.entry_button = customtkinter.CTkButton(master=self.group_frame, command=self.update_data_event,
                                                    text="Update Entries")
        self.entry_button.grid(row=1, column=2, pady=10, padx=20, sticky="n")

    # ----------------------------------This Generates the GPIB Group Frames--------------------------------------------
    @property
    def generate_single_frame(self):
        single_frame_tuple = []
        # Generate Single Form --> Head
        self.single_frame_title = customtkinter.CTkFrame(self.single_frame)
        self.single_frame_title.grid(row=0, column=0, padx=(5, 5), pady=(5, 5))
        self.single_frame_title_text = customtkinter.CTkLabel(self.single_frame_title, font=("Calibre", 16),
                                                              text="Instrument")
        self.single_frame_title_text.grid(row=0, column=0, padx=(5, 1))
        self.single_frame_title_val = customtkinter.CTkLabel(self.single_frame_title, font=("Calibre", 16),
                                                             text=self.single_frame_data.get("Instrument"))
        self.single_frame_title_val.grid(row=0, column=1, padx=(1, 5))
        single_frame_tuple.append(("Instrument", self.single_frame_title_val))

        # Generate Single Form --> Option Menu
        self.single_frame_mode = customtkinter.CTkFrame(self.single_frame, width=120)
        self.single_frame_mode.grid(row=1, column=0, padx=(5, 5), pady=(0, 5))
        single_frame_mode_values = ["Apply Incremental Voltage",
                                    "Apply Steady Voltage"]
        self.single_frame_option_menu = customtkinter.CTkOptionMenu(self.single_frame_mode,
                                                                    values=single_frame_mode_values,
                                                                    command=self.single_frame_mode_event)
        self.single_frame_option_menu.set(self.single_frame_data.get("OptionMenu"))
        self.single_frame_option_menu.grid(row=0, column=0, padx=20, pady=(5, 5))
        single_frame_tuple.append(("OptionMenu", self.single_frame_option_menu))
        # Generate the Single Form --> Labels & Entries
        # Form Line "row_counter" --> Label Will be updated ("row_counter")
        self.single_frame_form = customtkinter.CTkFrame(self.single_frame, width=120, corner_radius=0)
        self.single_frame_form.grid(row=2, column=0)
        row_counter = 0
        for label, entry in self.single_frame_data.items():
            if label != "Instrument" and label != "OptionMenu":
                self.single_frame_label = customtkinter.CTkLabel(self.single_frame_form, text=label)
                self.single_frame_label.grid(row=row_counter, column=0, sticky=tkinter.W, pady=2, padx=(5, 5))
                self.single_frame_entry = customtkinter.CTkEntry(self.single_frame_form)
                self.single_frame_entry.delete(0)
                self.single_frame_entry.insert(0, entry)
                self.single_frame_entry.grid(row=row_counter, column=1, pady=2, padx=(5, 5))
                single_frame_tuple.append((self.single_frame_label, self.single_frame_entry))
                row_counter += 1
        return single_frame_tuple

    # ------------------------------- This Updates the Number of GPIB Frames--------------------------------------------
    def sidebar_option_menu_event(self, new_appearance_mode: str):
        self.status_label_value.configure(text=new_appearance_mode)
        print("Status:", self.status_label_value.cget("text"))
        # ---------------- Generate frames relative to the inserted GPIB number
        self.group_data = []
        for i in range(0, int(self.status_label_value.cget("text"))):
            self.group_data.append({
                "Instrument": str(i + 1),
                "OptionMenu": "Apply Incremental Voltage",
                "Port Num": "GPIB::" + str(i),
                "Msnts Nums": str(i + 10),
                "Min Volt Set": str(i),
                "Max Volt Set": str(i + 10)
            })
        self.group_frame.destroy()
        self.generate_group_frame()

    # ------------------------------- This Updates the Single GPIB Operation--------------------------------------------
    def single_frame_mode_event(self, single_frame_mode: str):
        #-------------------------------------------------------------------------------------------------------------------------
        updated_group_data = []
        # ---------- Generate the new data based on the Intput from TK
        for single_group_data_tk in self.group_data_tk:
            single_group_data = dict(Instrument=single_group_data_tk[0][1].cget("text"),
                                     OptionMenu=single_group_data_tk[1][1].get())
            for i in range(2, len(single_group_data_tk)):
                single_group_data[str(single_group_data_tk[i][0].cget("text"))] = str(single_group_data_tk[i][1].get())
            updated_group_data.append(single_group_data)

        new_group_data = []
        for i in range(len(self.group_data)):
            print("Instrument: ", i + 1)
            previous_single_data = self.group_data[i]
            updated_single_data = updated_group_data[i]
            if previous_single_data["OptionMenu"]!=updated_single_data["OptionMenu"]:
                print("CHANGED")
                if updated_single_data["OptionMenu"] == "Apply Steady Voltage":
                    new_single_group_data = {
                            "Instrument": previous_single_data["Instrument"],
                            "OptionMenu": updated_single_data["OptionMenu"],
                            "Port Num": updated_single_data["Port Num"],
                            "Msnts Nums": updated_single_data["Msnts Nums"],
                            "Steady Volt Set": str(10),
                    }
                if updated_single_data["OptionMenu"] == "Apply Incremental Voltage":
                    new_single_group_data = {
                            "Instrument": previous_single_data["Instrument"],
                            "OptionMenu": updated_single_data["OptionMenu"],
                            "Port Num": updated_single_data["Port Num"],
                            "Msnts Nums": updated_single_data["Msnts Nums"],
                            "Min Volt Set": str(1),
                            "Max Volt Set": str(10)
                    }
                new_group_data.append(new_single_group_data)
            else: #<-------- if there is no change at the OptionMenu we keep it the same (previous)
                new_group_data.append(previous_single_data)

            #print("Before:", previous_single_data)
            print("   New:", new_group_data)
        self.group_data = new_group_data
        #-------------------------------------------------------------------------------------------------------------------------
        self.group_frame.destroy()
        self.generate_group_frame()

    def update_data_event(self):
        updated_group_data = []
        # ---------- Generate the new data based on the Intput from TK
        for single_group_data_tk in self.group_data_tk:
            single_group_data = dict(Instrument=single_group_data_tk[0][1].cget("text"),
                                     OptionMenu=single_group_data_tk[1][1].get())
            for i in range(2, len(single_group_data_tk)):
                single_group_data[str(single_group_data_tk[i][0].cget("text"))] = str(single_group_data_tk[i][1].get())
            updated_group_data.append(single_group_data)
        self.group_data = updated_group_data
        self.measure_event() # <--- a list of dictionaries, each dictornery is an instrument
        # print(self.group_data)

    def measure_event(self):
        task_result = Task_0_array(self.group_data)
        print(task_result)


    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

if __name__ == "__main__":
    app = App()
    app.mainloop()
