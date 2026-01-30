import customtkinter as ctk
from ui.app import SecurityToolkitApp

if __name__ == "__main__":
    # System settings
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("dark-blue")
    
    # Initialize App
    app = SecurityToolkitApp()
    app.title("AstraSecure")
    app.geometry("1100x700")
    
    # Run
    app.mainloop()
