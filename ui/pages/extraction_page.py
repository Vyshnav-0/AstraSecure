import customtkinter as ctk
from modules.hash_extractor import HashExtractor
import tkinter.messagebox as messagebox
import os

class ExtractionPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        
        self.extractor = HashExtractor()
        self.extracted_data = []

        # Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Header
        self.header = ctk.CTkFrame(self, fg_color="transparent")
        self.header.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        ctk.CTkLabel(self.header, text="Hash Extractor", font=("Roboto", 28, "bold")).pack(side="left")
        ctk.CTkLabel(self.header, text=" Parse/Import credentials from various sources.", text_color="gray70", font=("Roboto", 14)).pack(side="left", padx=10, pady=(10, 0))

        # --- Input Area ---
        self.card_input = ctk.CTkFrame(self, fg_color="#2b2b2b", corner_radius=15)
        self.card_input.grid(row=1, column=0, sticky="ew", padx=0, pady=10)
        self.card_input.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(self.card_input, text="Paste File Content (Linux Shadow or Windows Dump):", font=("Roboto", 14, "bold"), text_color="gray").grid(row=0, column=0, sticky="w", padx=20, pady=(20, 5))
        
        self.text_input = ctk.CTkTextbox(self.card_input, height=100, font=("Consolas", 11))
        self.text_input.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 10))
        self.text_input.insert("0.0", "root:$6$salt123$hashhashhash...:18000:0:99999:7:::\njohn:1001:NO_LM:8846F7EAEE8FB117AD06BDD830B7586C:::\n")
        
        self.frame_btns = ctk.CTkFrame(self.card_input, fg_color="transparent")
        self.frame_btns.grid(row=2, column=0, sticky="e", padx=20, pady=(0, 20))
        
        ctk.CTkButton(self.frame_btns, text="Load File...", width=100, command=self.load_file).pack(side="left", padx=5)
        ctk.CTkButton(self.frame_btns, text="EXTRACT HASHES", width=150, font=("Roboto", 12, "bold"), command=self.extract).pack(side="left", padx=5)

        # --- Output / Table Area ---
        self.card_out = ctk.CTkFrame(self, fg_color="#2b2b2b", corner_radius=15)
        self.card_out.grid(row=2, column=0, sticky="nsew", padx=0, pady=10)
        self.card_out.grid_columnconfigure(0, weight=1)
        self.card_out.grid_rowconfigure(1, weight=1)
        
        ctk.CTkLabel(self.card_out, text="Extracted Credentials", font=("Roboto", 14, "bold"), text_color="gray").grid(row=0, column=0, sticky="w", padx=20, pady=(20, 5))
        
        self.text_out = ctk.CTkTextbox(self.card_out, font=("Consolas", 12), text_color="#00ff00", fg_color="#1a1a1a")
        self.text_out.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))

        # Export Btn
        ctk.CTkButton(self.card_out, text="Save to CSV for Attack", fg_color="#2b8d45", command=self.save_csv).grid(row=2, column=0, pady=(0, 20))

    def load_file(self):
        f = ctk.filedialog.askopenfilename()
        if f:
            with open(f, 'r') as file:
                content = file.read()
                self.text_input.delete("0.0", "end")
                self.text_input.insert("0.0", content)

    def extract(self):
        content = self.text_input.get("0.0", "end").strip()
        if not content: return
        
        self.extracted_data = [] # Reset
        
        # Try Linux first
        linux_res = self.extractor.parse_linux_shadow(content)
        win_res = self.extractor.parse_windows_dump(content)
        csv_res = self.extractor.parse_csv_dump(content)
        
        self.extracted_data.extend(linux_res)
        self.extracted_data.extend(win_res)
        self.extracted_data.extend(csv_res)
        
        self.text_out.delete("0.0", "end")
        
        if not self.extracted_data:
            self.text_out.insert("0.0", "// No valid hash patterns found.\n")
            return
            
        header = f"{'USER':<15} | {'ALGO':<15} | {'HASH (Snippet)'}"
        self.text_out.insert("end", header + "\n" + "-"*60 + "\n")
        
        for item in self.extracted_data:
            h_snip = item['hash'][:20] + "..."
            line = f"{item['username']:<15} | {item['algorithm']:<15} | {h_snip}\n"
            self.text_out.insert("end", line)
            
        self.text_out.insert("end", "\n" + "-"*60 + "\n")
        self.text_out.insert("end", f"Total Extracted: {len(self.extracted_data)}")

    def save_csv(self):
        if not self.extracted_data: return
        try:
            filename = "extracted_hashes.csv"
            import csv
            with open(filename, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Username", "Hash_Value", "Algorithm"])
                for item in self.extracted_data:
                    writer.writerow([item['username'], item['hash'], item['algorithm']])
            messagebox.showinfo("Saved", f"Exported to {os.path.abspath(filename)}\nYou can now load this file in the Attack Simulator.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
