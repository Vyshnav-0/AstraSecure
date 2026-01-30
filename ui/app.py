import customtkinter as ctk
import os
from PIL import Image, ImageTk

class SecurityToolkitApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # THEME SETUP
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("dark-blue")
        
        # Colors & Fonts
        self.c_sidebar = "#1a1a1a"
        self.c_bg = "#242424"
        self.c_accent = "#1f538d"
        self.c_hover = "#14375e"
        self.font_head = ("Roboto Medium", 20)
        self.font_body = ("Roboto", 14)

        self.title("AstraSecure")
        self.geometry("1280x800")
        
        # Icon Setup
        try:
            if os.path.exists("icon.png"):
                icon_img = ImageTk.PhotoImage(Image.open("icon.png"))
                self.iconphoto(False, icon_img)
                self.wm_iconbitmap() # attempt to clear default
        except Exception as e:
            print(f"Warning: Could not load icon.png: {e}")
        
        # Configure Grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Sidebar ---
        self.sidebar_frame = ctk.CTkFrame(self, width=250, corner_radius=0, fg_color=self.c_sidebar)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(10, weight=1)

        # Logo
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="🛡️ AstraSecure", 
                                     font=("Roboto", 26, "bold"), text_color="white")
        self.logo_label.grid(row=0, column=0, padx=20, pady=(40, 30))

        # Nav Buttons
        self.nav_buttons = {}
        self.create_nav_button("Dictionary Generator", self.show_dictionary_page, 1)
        self.create_nav_button("Hash Manager", self.show_hash_page, 2)
        self.create_nav_button("Hash Extractor", self.show_extraction_page, 3)
        self.create_nav_button("Brute Force Sim", self.show_bruteforce_page, 4)
        self.create_nav_button("Dictionary Attack", self.show_dict_attack_page, 5)
        self.create_nav_button("Strength Analyzer", self.show_strength_page, 6)
        self.create_nav_button("Audit Reports", self.show_report_page, 7)
        
        # Version Info
        self.ver_label = ctk.CTkLabel(self.sidebar_frame, text="v1.0.0 Pro", text_color="gray50", font=("Roboto", 12))
        self.ver_label.grid(row=10, column=0, pady=20)

        # --- Main Content Area ---
        self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color=self.c_bg)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        
        # Container for pages to add padding
        self.page_container = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.page_container.pack(fill="both", expand=True, padx=30, pady=30)

        self.current_page = None
        self.active_btn = None
        
        # Init
        self.show_dictionary_page()

    def create_nav_button(self, text, command, row):
        btn = ctk.CTkButton(self.sidebar_frame, text=text, command=lambda: self.select_nav(command, text),
                            height=45, 
                            corner_radius=8,
                            fg_color="transparent", 
                            hover_color=self.c_hover,
                            anchor="w", 
                            font=self.font_body)
        btn.grid(row=row, column=0, sticky="ew", padx=15, pady=5)
        self.nav_buttons[text] = btn

    def select_nav(self, command, name):
        # Reset buttons
        for btn in self.nav_buttons.values():
            btn.configure(fg_color="transparent", text_color="gray90")
        
        # Highlight active
        self.nav_buttons[name].configure(fg_color=self.c_accent, text_color="white")
        
        # Run command
        command()

    def clear_main_frame(self):
        for widget in self.page_container.winfo_children():
            widget.destroy()

    def show_dictionary_page(self):
        self.clear_main_frame()
        self.select_nav(lambda: None, "Dictionary Generator") # Ensure visual select
        from ui.pages.dictionary_page import DictionaryPage
        self.current_page = DictionaryPage(self.page_container)
        self.current_page.pack(fill="both", expand=True)

    def show_hash_page(self):
        self.clear_main_frame()
        from ui.pages.hash_page import HashPage
        self.current_page = HashPage(self.page_container)
        self.current_page.pack(fill="both", expand=True)

    def show_extraction_page(self):
        self.clear_main_frame()
        from ui.pages.extraction_page import ExtractionPage
        self.current_page = ExtractionPage(self.page_container)
        self.current_page.pack(fill="both", expand=True)


    def show_bruteforce_page(self):
        self.clear_main_frame()
        from ui.pages.bruteforce_page import BruteForcePage
        self.current_page = BruteForcePage(self.page_container)
        self.current_page.pack(fill="both", expand=True)

    def show_dict_attack_page(self):
        self.clear_main_frame()
        from ui.pages.dict_attack_page import DictionaryAttackPage
        self.current_page = DictionaryAttackPage(self.page_container)
        self.current_page.pack(fill="both", expand=True)
        
    def show_strength_page(self):
        self.clear_main_frame()
        from ui.pages.strength_page import StrengthPage
        self.current_page = StrengthPage(self.page_container)
        self.current_page.pack(fill="both", expand=True)

    def show_report_page(self):
        self.clear_main_frame()
        from ui.pages.report_page import ReportPage
        self.current_page = ReportPage(self.page_container)
        self.current_page.pack(fill="both", expand=True)
