import time
import tkinter
import tkinter.messagebox
import customtkinter

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        # -----------------------------------------------------Window---------------------------------------------------
        # configure window
        self.group_frame = None
        self.single_frame = None
        self.single_frame_entry = None
        self.title("Keithley Console")
        self.geometry(f"{900}x{480}")
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
        self.sidebar_gpib_label = customtkinter.CTkLabel(self.sidebar_frame, text="Select Number of GPIBs:", anchor="w")
        self.sidebar_gpib_label.grid(row=0, column=0, padx=20, pady=(10, 0))
        # Side Bar --> Option Menu
        gpib_optionemenu_values = ["0", "1", "2", "3", "4", "5", "6", "7"]
        self.sidebar_gpib_optionmenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=gpib_optionemenu_values,
                                                                    command=self.gpib_option_menu_event)
        self.sidebar_gpib_optionmenu.set("2")
        self.sidebar_gpib_optionmenu.grid(row=1, column=0, padx=20, pady=(10, 10))



        # Side Bar --> Appearance Mode
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        # Side Bar --> Window Scale
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.set("100%")
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # ------------------------------------------------Main Frame----------------------------------------------------
        # Create Main Frame with widgets
        self.main_frame = customtkinter.CTkScrollableFrame(self, width=180, height=400, corner_radius=0)
        self.main_frame.grid(row=0, column=1, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.main_frame.grid_rowconfigure(4, weight=1)
        # Main Frame --> Labels Will be updated
        self.status_label_title = customtkinter.CTkLabel(self.main_frame, text="Number of GPIBs:", font=("Calibri", 18))
        self.status_label_title.grid(row=0, column=0, padx=5, pady=(10, 0))
        self.status_label_value = customtkinter.CTkLabel(self.main_frame, text="2", font=("Calibri", 18))
        self.status_label_value.grid(row=0, column=1, pady=(10, 0))

        # Main Frame --> Generate Individual Frame Data for each GPIB
        print("Status:",self.status_label_value.cget("text"))
        # "group_data" refer to all the data which will be completed and will be sent to the GPIBs
        # "group_data_tk" refer to all the tk data relevant to the group_data which operate the UI
        self.group_data = [] # 3D-Array (1st: the individual frame; 2nd: the label; 3rd: the entry)
        default_frame_A = [["Mode:","DC volt"],
                        ["Port Num:","GPIB::3"],
                        ["Msnts Nums:","10"],
                        ["Min Volt Set:","1"],
                        ["Max Volt Set:","10"]]
        self.group_data.append(default_frame_A)
        default_frame_B = [["Port Num:","GPIB::6"],
                        ["Msnts Nums:","20"],
                        ["Min Volt Set:","5"],
                        ["Max Volt Set:","15"]]
        self.group_data.append(default_frame_B)
        self.group_data_tk = self.generate_group_frame()

    # ----------------------------------This Generates the GPIB Group Frames--------------------------------------------
    def generate_group_frame(self):
        # Group Frame which includes GPIBs
        self.group_frame = customtkinter.CTkFrame(self.main_frame, width=160, corner_radius=0)
        self.group_frame.grid(row=2, column=2, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.group_frame.grid_rowconfigure(1, weight=1)
        group_frame_tk_data = []
        for i in range(0, int(self.status_label_value.cget("text"))):
            # Single Frame
            self.single_frame = customtkinter.CTkFrame(self.group_frame, width=190)
            self.single_frame.grid(row=i + 1, column=1, padx=(5, 5), pady=(5, 10), sticky="nsew")
            self.single_frame_data = self.group_data[i]
            group_frame_tk_data.append(self.generate_single_frame('Instrument '+str(i+1)))
        self.enty_button = customtkinter.CTkButton(master=self.group_frame, command=self.update_label, text="START")
        self.enty_button.grid(row=1, column=2, pady=10, padx=20, sticky="n")
        return group_frame_tk_data

    # ----------------------------------This Generates the GPIB Group Frames--------------------------------------------
    def generate_single_frame(self, field_head):
        # Form Head
        self.single_frame_title = customtkinter.CTkLabel(self.single_frame, text=field_head, font=("Calibri", 16))
        self.single_frame_title.grid(row=0, column=0, padx=(5, 5))

        single_frame_tuple = []
        self.single_frame_mode = customtkinter.CTkFrame(self.single_frame, width=120)
        self.single_frame_mode.grid(row=1, column=0, padx=(5, 5), pady=(0, 5))
        single_frame_mode_values = ["Apply Steady Voltage", "Apply Incremental Voltage"]
        self.single_frame_optionmenu = customtkinter.CTkOptionMenu(self.single_frame_mode, values=single_frame_mode_values,
                                                                    command=self.single_frame_mode_event)
        self.single_frame_optionmenu.set("Apply Incremental Voltage")
        self.single_frame_optionmenu.grid(row=0, column=0, padx=20, pady=(5, 5))
        single_frame_tuple.append(self.single_frame_optionmenu)

        # Generate the Single Form
        single_frame_tuple = self.generate_single_form(single_frame_tuple)
        return single_frame_tuple

    # ----------------------------------Single Form Generator ----------------------------------------------------------
    def generate_single_form(self, single_frame_tuple):
        # Form Line "i" --> Label Will be updated ("i")
        self.single_frame_form = customtkinter.CTkFrame(self.single_frame, width=120, corner_radius=0)
        self.single_frame_form.grid(row=2, column=0)
        for i in range(0, len(self.single_frame_data)):
            self.single_frame_label = customtkinter.CTkLabel(self.single_frame_form, text=self.single_frame_data[i][0])
            self.single_frame_label.grid(row = i, column = 0, sticky = tkinter.W, pady = 2, padx=(5, 5))
            self.single_frame_entry = customtkinter.CTkEntry(self.single_frame_form)
            self.single_frame_entry.delete(0)
            self.single_frame_entry.insert(0, self.single_frame_data[i][1])
            self.single_frame_entry.grid(row = i, column = 1, pady = 2, padx=(5, 5))
            single_frame_tuple.append(self.single_frame_label)
            single_frame_tuple.append(self.single_frame_entry)
        return(single_frame_tuple)


    # ------------------------------- This Updates the Number of GPIB Frames--------------------------------------------
    def gpib_option_menu_event(self, new_appearance_mode: str):
        self.status_label_value.configure(text=new_appearance_mode)
        #---------------- Generate frames relative to the inserted GPIB number
        self.group_data = []
        for i in range(0,int(self.status_label_value.cget("text"))):
            self.group_data.append([["Port Num:","GPIB::"+str(i)],
                        ["Msnts Nums:",str(i+10)],
                        ["Min Volt Set:",str(i)],
                        ["Max Volt Set:",str(i+10)]])
        self.group_frame.destroy()
        self.group_data_tk = self.generate_group_frame()

    # ------------------------------- This Updates the Single GPIB Operation--------------------------------------------
    def single_frame_mode_event(self, single_frame_mode: str):
        print(single_frame_mode,"---")
        print(self.single_frame_optionmenu.get(),"++")
        default_frame_C = [["Port Num:","GPIB::9"],
                        ["Msnts Nums:","30"],
                        ["Min Volt Set:","15"],
                        ["Max Volt Set:","25"]]
       #self.single_frame_form.destroy()
        # Generate the Single Form
        single_frame_tuple = []
        #single_frame_tuple.append(self.single_frame_optionmenu)
        #single_frame_tuple = self.generate_single_form(single_frame_tuple)
        return single_frame_tuple

    def update_label(self):
        current_group_data_tk = self.group_data_tk
        for field in current_group_data_tk:
            mode =  field[0].get()
            print("---(Mode)---", mode)
            label = field[1].cget("text")
            entry = field[2].get()
            print("---(Lable 1)---", label, "-->", entry)
            #label = field[3].cget("text")
            #entry = field[4].get()
            #print("---(Lable 2)---", label, "-->", entry)

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

if __name__ == "__main__":
    app = App()
    app.mainloop()
