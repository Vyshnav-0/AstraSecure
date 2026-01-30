import customtkinter as ctk
from modules.dictionary_generator import DictionaryGenerator
import tkinter.messagebox as messagebox
import os


class DictionaryPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        
        self.generator = DictionaryGenerator()

        # Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Header
        self.header = ctk.CTkFrame(self, fg_color="transparent")
        self.header.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        ctk.CTkLabel(self.header, text="Dictionary Generator", font=("Roboto", 28, "bold")).pack(side="left")
        ctk.CTkLabel(self.header, text=" Create wordlists using Personal Info.", text_color="gray70", font=("Roboto", 14)).pack(side="left", padx=10, pady=(10, 0))

        # --- Tabs ---
        self.tabview = ctk.CTkTabview(self, fg_color="#2b2b2b")
        self.tabview.grid(row=1, column=0, sticky="nsew", padx=10, pady=0)
        self.tabview.grid_columnconfigure(0, weight=1)
        
        self.tab_personal = self.tabview.add("Targeted (Personal)")
        self.setup_targeted_tab()


        # --- Output / Preview Area ---
        self.preview_frame = ctk.CTkFrame(self, fg_color="#1a1a1a", corner_radius=10)
        self.preview_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=20)
        self.preview_frame.grid_columnconfigure(0, weight=1)
        self.preview_frame.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(self.preview_frame, text="Generation Log / Preview", font=("Roboto", 12, "bold"), text_color="gray").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        
        self.textbox = ctk.CTkTextbox(self.preview_frame, font=("Consolas", 12), fg_color="transparent", text_color="#00ff00")
        self.textbox.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        
    def setup_targeted_tab(self):
        # Base Words
        ctk.CTkLabel(self.tab_personal, text="Base Words (Names, Company, etc):").pack(anchor="w", padx=20, pady=(20, 5))
        self.entry_base = ctk.CTkEntry(self.tab_personal, placeholder_text="e.g. admin, john, secret")
        self.entry_base.pack(fill="x", padx=20, pady=5)

        # DOB
        ctk.CTkLabel(self.tab_personal, text="Target Year / DOB (Optional):").pack(anchor="w", padx=20, pady=5)
        self.entry_dob = ctk.CTkEntry(self.tab_personal, placeholder_text="e.g. 1995")
        self.entry_dob.pack(fill="x", padx=20, pady=5)

        # Options
        self.opts_frame = ctk.CTkFrame(self.tab_personal, fg_color="transparent")
        self.opts_frame.pack(fill="x", padx=10, pady=10)
        
        self.var_leet = ctk.BooleanVar(value=True)
        self.var_case = ctk.BooleanVar(value=True)
        self.var_nums = ctk.BooleanVar(value=True)
        self.var_syms = ctk.BooleanVar(value=True)

        ctk.CTkCheckBox(self.opts_frame, text="Leetspeak", variable=self.var_leet).pack(side="left", padx=10)
        ctk.CTkCheckBox(self.opts_frame, text="Case Variants", variable=self.var_case).pack(side="left", padx=10)
        ctk.CTkCheckBox(self.opts_frame, text="Add Numbers", variable=self.var_nums).pack(side="left", padx=10)
        ctk.CTkCheckBox(self.opts_frame, text="Add Symbols", variable=self.var_syms).pack(side="left", padx=10)

        # Button
        ctk.CTkButton(self.tab_personal, text="GENERATE TARGETED LIST", command=self.generate_personal, 
                      height=40, font=("Roboto", 14, "bold")).pack(fill="x", padx=20, pady=20)



    def generate_personal(self):
        base = self.entry_base.get()
        dob = self.entry_dob.get()
        if not base: return
        
        try:
            self.textbox.delete("1.0", "end")
            self.textbox.insert("end", "[*] Generating Targeted Wordlist...\n")
            
            res = self.generator.generate_custom_list(
                base.split(","), bool(dob), dob, 
                self.var_leet.get(), self.var_case.get(), self.var_nums.get(), self.var_syms.get()
            )
            
            self.textbox.insert("end", f"[+] Generated {len(res)} words.\n")
            self.generator.save_to_file(res, "generated_dict.txt")
            self.textbox.insert("end", f"[+] Saved to: {os.path.abspath('generated_dict.txt')}\n")
            
            # Preview
            self.textbox.insert("end", "\n--- PREVIEW ---\n")
            self.textbox.insert("end", "\n".join(res[:50]))
            
        except Exception as e:
            messagebox.showerror("Error", str(e))


