import customtkinter as ctk
from modules.hash_manager import HashManager
import tkinter.messagebox as messagebox
import os

class HashPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        
        self.manager = HashManager()

        # Grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Header
        self.header = ctk.CTkFrame(self, fg_color="transparent")
        self.header.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 20))
        ctk.CTkLabel(self.header, text="Hash Manager", font=("Roboto", 28, "bold")).pack(side="left")
        ctk.CTkLabel(self.header, text=" Generate safe test hashes.", text_color="gray70", font=("Roboto", 14)).pack(side="left", padx=10, pady=(10, 0))

        # --- Card 1: Single Hash (Left) ---
        self.card_single = ctk.CTkFrame(self, fg_color="#2b2b2b", corner_radius=15)
        self.card_single.grid(row=1, column=0, sticky="nsew", padx=(0, 10), pady=10)
        self.card_single.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(self.card_single, text="Single Password Hash", font=("Roboto", 16, "bold")).grid(row=0, column=0, columnspan=2, sticky="w", padx=20, pady=20)
        
        self.entry_single = ctk.CTkEntry(self.card_single, placeholder_text="Enter password...", height=40)
        self.entry_single.grid(row=1, column=0, columnspan=2, sticky="ew", padx=20, pady=(0, 15))

        ctk.CTkLabel(self.card_single, text="Algorithm:", font=("Roboto", 12)).grid(row=2, column=0, padx=20, sticky="w")
        self.combo_algo = ctk.CTkComboBox(self.card_single, values=["MD5", "SHA256", "SHA512"], width=120)
        self.combo_algo.grid(row=2, column=1, padx=20, sticky="e")
        self.combo_algo.set("SHA256")

        self.btn_single = ctk.CTkButton(self.card_single, text="HASH IT", command=self.run_single_hash, 
                                        height=40, font=("Roboto", 12, "bold"), fg_color="#1f538d")
        self.btn_single.grid(row=3, column=0, columnspan=2, padx=20, pady=20, sticky="ew")

        # --- Card 2: Bulk File (Right) ---
        self.card_bulk = ctk.CTkFrame(self, fg_color="#2b2b2b", corner_radius=15)
        self.card_bulk.grid(row=1, column=1, sticky="nsew", padx=(10, 0), pady=10)
        self.card_bulk.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(self.card_bulk, text="Bulk File Processing", font=("Roboto", 16, "bold")).grid(row=0, column=0, columnspan=2, sticky="w", padx=20, pady=20)

        self.entry_file = ctk.CTkEntry(self.card_bulk, placeholder_text="dictionary.txt", height=40)
        self.entry_file.grid(row=1, column=0, sticky="ew", padx=(20, 5), pady=(0, 15))
        
        self.btn_browse = ctk.CTkButton(self.card_bulk, text="...", width=40, height=40, command=self.browse_file)
        self.btn_browse.grid(row=1, column=1, padx=(0, 20), pady=(0, 15))

        self.btn_bulk = ctk.CTkButton(self.card_bulk, text="GENERATE LIST", command=self.run_bulk, 
                                      height=40, font=("Roboto", 12, "bold"), fg_color="#2b8d45") # Green for "Go"
        self.btn_bulk.grid(row=3, column=0, columnspan=2, padx=20, pady=20, sticky="ew")

        # --- Output Area (Bottom) ---
        self.out_frame = ctk.CTkFrame(self, fg_color="#2b2b2b", corner_radius=15)
        self.out_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=(10, 0))
        self.out_frame.grid_rowconfigure(1, weight=1)
        self.out_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(self.out_frame, text="Log Output", font=("Roboto", 14, "bold"), text_color="gray").grid(row=0, column=0, sticky="w", padx=20, pady=10)
        
        self.textbox = ctk.CTkTextbox(self.out_frame, font=("Consolas", 12), fg_color="#1a1a1a")
        self.textbox.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))

    def run_single_hash(self):
        pwd = self.entry_single.get()
        if not pwd: 
            return
        algo = self.combo_algo.get()
        h = self.manager.hash_password(pwd, algo)
        self.textbox.insert("0.0", f"[{algo}] {pwd} -> {h}\n")

    def browse_file(self):
        file = ctk.filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file:
            self.entry_file.delete(0, "end")
            self.entry_file.insert(0, file)

    def run_bulk(self):
        path = self.entry_file.get()
        if not path or not os.path.exists(path):
            messagebox.showerror("Error", "Valid file path required")
            return
            
        try:
            words = self.manager.load_wordlist(path)
            algo = self.combo_algo.get()
            
            # Limit
            if len(words) > 10000:
                words = words[:10000]
                self.textbox.insert("0.0", "Warning: Limiting to first 10,000 words.\n")

            hash_pairs = self.manager.generate_hash_list(words, algo)
            saved_file = self.manager.save_hashes(hash_pairs, algo)
            
            self.textbox.insert("0.0", f"Success! Hashes saved to: {os.path.abspath(saved_file)}\n")
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
