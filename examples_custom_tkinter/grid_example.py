import tkinter
import tkinter.messagebox
import customtkinter

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

# ----------------------------- Grid Rules -----------------------------
# The Grid geometry manager puts the widgets in a 2-dimensional table
# The Tkinter Grid has two types of positions
# Absolute --> is the position relative to the **window**
# Relative --> is the position relative to the **frame**
# These positions are defined based on the master argument of the widget
# If the master=root/self then the widget position is Absolute
# If the master=root/self.Frame then the widget position is Relative
# -----------------------------------------------------------------------

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("CustomTkinter complex_example.py")
        self.geometry(f"{1100}x{780}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # Frame with Absolute position (row=0, column=0)
        # every additional widget included in this frame will have relative position to this frame
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        # Label with Relative position (row=0, column=0)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Label (row=0, column=0)", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        # Label with Relative position (row=1, column=0)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Label (row=1, column=0)", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=1, column=0, padx=20, pady=(20, 10))

        # Label with Absolute position (row=0, column=1)
        self.logo_label = customtkinter.CTkLabel(self, text="Label (row=1, column=0)", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=1, padx=20, pady=(20, 10))
        # Label with Absolute position (row=1, column=1)
        self.logo_label = customtkinter.CTkLabel(self, text="Label (row=1, column=0)", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=1, column=1, padx=20, pady=(20, 10))

        # Frame with Absolute position (row=0, column=2)
        # every additional widget included in this frame will have relative position to this frame
        self.sidebar_frame = customtkinter.CTkFrame(self)
        self.sidebar_frame.grid(row=0, column=2,  padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        # Label with Relative position (row=0, column=0)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Label (row=0, column=0)", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        # Label with Relative position (row=1, column=0)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Label (row=1, column=0)", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=1, column=0, padx=20, pady=(20, 10))

        # Frame with Absolute position (row=1, column=2)
        # every additional widget included in this frame will have relative position to this frame
        self.sidebar_frame = customtkinter.CTkFrame(self)
        self.sidebar_frame.grid(row=1, column=2,  padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        # Label with Relative position (row=0, column=0)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Label (row=0, column=0)", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        # Label with Relative position (row=1, column=0)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Label (row=1, column=0)", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=1, column=0, padx=20, pady=(20, 10))

        # Label with columnspan
        self.logo_label = customtkinter.CTkLabel(self, text="Label (1,0)", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

if __name__ == "__main__":
    app = App()
    app.mainloop()
