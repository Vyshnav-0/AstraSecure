import customtkinter as ctk
from modules.strength_analyzer import StrengthAnalyzer

class StrengthPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        
        self.analyzer = StrengthAnalyzer()

        # Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Header
        self.header = ctk.CTkFrame(self, fg_color="transparent")
        self.header.grid(row=0, column=0, sticky="ew", pady=(0, 40))
        ctk.CTkLabel(self.header, text="Strength Analyzer", font=("Roboto", 28, "bold")).pack()
        ctk.CTkLabel(self.header, text="How tough is your password?", text_color="gray70", font=("Roboto", 16)).pack(pady=5)

        # --- Input Area (Centered) ---
        self.card_input = ctk.CTkFrame(self, fg_color="#2b2b2b", corner_radius=20)
        self.card_input.grid(row=1, column=0, sticky="ew", padx=100) # Centered with large padding
        self.card_input.grid_columnconfigure(0, weight=1)
        
        self.entry_pwd = ctk.CTkEntry(self.card_input, placeholder_text="Type a password to test...", 
                                      height=60, font=("Roboto", 20), show="*")
        self.entry_pwd.grid(row=0, column=0, sticky="ew", padx=30, pady=30)
        self.entry_pwd.bind("<KeyRelease>", self.check_strength)
        
        self.cb_show = ctk.CTkCheckBox(self.card_input, text="Reveal", command=self.toggle_show, font=("Roboto", 12))
        self.cb_show.grid(row=1, column=0, pady=(0, 20))

        # --- Result Area ---
        self.res_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.res_frame.grid(row=2, column=0, sticky="nsew", pady=30)
        self.res_frame.grid_columnconfigure(0, weight=1)
        
        # Rating Text
        self.lbl_rating = ctk.CTkLabel(self.res_frame, text="...", font=("Roboto", 36, "bold"), text_color="gray")
        self.lbl_rating.pack(pady=10)
        
        # Progress Bar
        self.progress = ctk.CTkProgressBar(self.res_frame, width=500, height=15)
        self.progress.pack(pady=20)
        self.progress.set(0)
        
        # Stats Grid
        self.stats_frame = ctk.CTkFrame(self.res_frame, fg_color="transparent")
        self.stats_frame.pack(pady=10)
        
        self.card_ent = self.create_stat_card(self.stats_frame, "Entropy", "0 bits", 0)
        self.card_time = self.create_stat_card(self.stats_frame, "Crack Time", "Instant", 1)

        # Suggestions
        self.lbl_sugg = ctk.CTkLabel(self.res_frame, text="", font=("Roboto", 14), text_color="orange")
        self.lbl_sugg.pack(pady=30)

    def create_stat_card(self, parent, title, value, col):
        frame = ctk.CTkFrame(parent, fg_color="#333", corner_radius=10, width=200, height=80)
        frame.grid(row=0, column=col, padx=10)
        frame.pack_propagate(False) # fixed size
        
        ctk.CTkLabel(frame, text=title, font=("Roboto", 12), text_color="gray").pack(pady=(15, 0))
        lbl_val = ctk.CTkLabel(frame, text=value, font=("Roboto", 16, "bold"), text_color="white")
        lbl_val.pack(pady=5)
        return lbl_val

    def toggle_show(self):
        if self.entry_pwd.cget("show") == "*":
            self.entry_pwd.configure(show="")
        else:
            self.entry_pwd.configure(show="*")

    def check_strength(self, event=None):
        pwd = self.entry_pwd.get()
        if not pwd:
            self.reset_ui()
            return
            
        res = self.analyzer.evaluate_strength(pwd)
        
        # Update UI
        self.lbl_rating.configure(text=res['rating'])
        self.card_ent.configure(text=f"{res['entropy']} bits")
        self.card_time.configure(text=res['crack_time_display'])
        
        if res['suggestions']:
            self.lbl_sugg.configure(text="\n".join(res['suggestions']))
        else:
            self.lbl_sugg.configure(text="Great password! No suggestions.", text_color="#00ff00")
            
        # Colors
        score = res['score']
        colors = {1: "#ff3333", 2: "#ff9933", 3: "#ffcc00", 4: "#99cc33", 5: "#33cc33"}
        c = colors.get(score, "gray")
        
        self.lbl_rating.configure(text_color=c)
        self.progress.configure(progress_color=c)
        self.progress.set(score / 5)

    def reset_ui(self):
        self.lbl_rating.configure(text="...", text_color="gray")
        self.progress.set(0)
        self.card_ent.configure(text="0 bits")
        self.card_time.configure(text="Instant")
        self.lbl_sugg.configure(text="")
