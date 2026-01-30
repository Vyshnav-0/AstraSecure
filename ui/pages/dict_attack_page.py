import customtkinter as ctk
from modules.dictionary_attack import DictionaryAttacker
import threading
import tkinter.messagebox as messagebox
import os
import time

class DictionaryAttackPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        
        self.attacker = DictionaryAttacker()
        self.attack_thread = None

        # Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(5, weight=1)

        # Title
        self.title = ctk.CTkLabel(self, text="Dictionary Attack Simulator", font=ctk.CTkFont(size=24, weight="bold"))
        self.title.grid(row=0, column=0, pady=(10, 5), sticky="w")
        
        self.desc = ctk.CTkLabel(self, text="Crack a list of hashes using a wordlist.", text_color="gray")
        self.desc.grid(row=1, column=0, pady=(0, 20), sticky="w")

        # Inputs Frame
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.grid(row=2, column=0, sticky="ew", pady=10)
        self.input_frame.grid_columnconfigure(1, weight=1)

        # Hash File
        ctk.CTkLabel(self.input_frame, text="Hash List (CSV):").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.entry_hash_file = ctk.CTkEntry(self.input_frame, placeholder_text="Path to test_hashes.csv")
        self.entry_hash_file.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        ctk.CTkButton(self.input_frame, text="Browse", width=60, command=self.browse_hash).grid(row=0, column=2, padx=10)

        # Dictionary File
        ctk.CTkLabel(self.input_frame, text="Dictionary (TXT):").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.entry_dict_file = ctk.CTkEntry(self.input_frame, placeholder_text="Path to dictionary.txt")
        self.entry_dict_file.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        ctk.CTkButton(self.input_frame, text="Browse", width=60, command=self.browse_dict).grid(row=1, column=2, padx=10)

        # Algorithm
        ctk.CTkLabel(self.input_frame, text="Algorithm used:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.combo_algo = ctk.CTkComboBox(self.input_frame, values=["SHA256", "MD5", "SHA512"])
        self.combo_algo.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        # Controls
        self.btn_run = ctk.CTkButton(self, text="START DICTIONARY ATTACK", height=40, font=ctk.CTkFont(size=15, weight="bold"), command=self.start_attack)
        self.btn_run.grid(row=3, column=0, pady=20, sticky="ew")

        # Stats
        self.lbl_stats = ctk.CTkLabel(self, text="Status: Ready")
        self.lbl_stats.grid(row=4, column=0, pady=5)

        # Results
        self.res_frame = ctk.CTkFrame(self)
        self.res_frame.grid(row=5, column=0, sticky="nsew")
        self.res_frame.grid_columnconfigure(0, weight=1)
        self.res_frame.grid_rowconfigure(1, weight=1)
        
        ctk.CTkLabel(self.res_frame, text="Cracked Passwords:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, sticky="w", padx=10, pady=5)
        
        self.textbox = ctk.CTkTextbox(self.res_frame)
        self.textbox.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)

    def browse_hash(self):
        f = ctk.filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if f: 
            self.entry_hash_file.delete(0, "end")
            self.entry_hash_file.insert(0, f)

    def browse_dict(self):
        f = ctk.filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if f: 
            self.entry_dict_file.delete(0, "end")
            self.entry_dict_file.insert(0, f)

    def update_status(self, attempts, cracked_count):
        self.lbl_stats.configure(text=f"Running... Checked: {attempts:,} | Cracked: {cracked_count}")

    def start_attack(self):
        hash_file = self.entry_hash_file.get()
        dict_file = self.entry_dict_file.get()
        algo = self.combo_algo.get()
        
        if not os.path.exists(hash_file) or not os.path.exists(dict_file):
            messagebox.showerror("Error", "Invalid file paths")
            return
            
        self.btn_run.configure(state="disabled", text="Running...")
        self.textbox.delete("0.0", "end")
        
        self.attack_thread = threading.Thread(target=self.run_logic, args=(hash_file, dict_file, algo))
        self.attack_thread.start()

    def run_logic(self, hash_file, dict_file, algo):
        try:
            # 1. Load Targets
            targets, count = self.attacker.load_targets(hash_file)
            self.textbox.insert("end", f"Loaded {count} hashes to crack.\n")
            
            # 2. Run Attack
            start_time = time.time()
            results = self.attacker.attack(targets, dict_file, algo, 
                                           callback_status=lambda a, c: self.after(0, lambda: self.update_status(a, c)))
            
            end_time = time.time()
            
            # 3. Report
            self.after(0, lambda: self.show_results(results, end_time - start_time))
            
        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Error", str(e)))
            self.after(0, lambda: self.btn_run.configure(state="normal", text="START DICTIONARY ATTACK"))

    def show_results(self, results, duration):
        self.btn_run.configure(state="normal", text="START DICTIONARY ATTACK")
        self.lbl_stats.configure(text=f"Finished in {duration:.2f}s")
        
        self.textbox.insert("end", "\n" + "="*30 + "\n")
        self.textbox.insert("end", f"ATTACK COMPLETE\nFound {len(results)} passwords:\n\n")
        
        for pwd, h in results:
            self.textbox.insert("end", f"CRACKED: {pwd}  (Hash: {h[:10]}...)\n")
            
        if not results:
            self.textbox.insert("end", "No matches found in this dictionary.\n")
