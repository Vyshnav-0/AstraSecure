import customtkinter as ctk
from modules.report_generator import ReportGenerator
import tkinter.messagebox as messagebox
import os
import threading

class ReportPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        
        self.generator = ReportGenerator()

        # Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        # Title
        self.title_label = ctk.CTkLabel(self, text="Security Audit Reporter", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.grid(row=0, column=0, pady=(10, 5), sticky="w")
        
        self.desc_label = ctk.CTkLabel(self, text="Generate a comprehensive risk report based on your lab data.", text_color="gray")
        self.desc_label.grid(row=1, column=0, pady=(0, 20), sticky="w")

        # Configuration Frame
        self.conf = ctk.CTkFrame(self)
        self.conf.grid(row=2, column=0, sticky="ew", pady=10)
        self.conf.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(self.conf, text="Hash Database:").grid(row=0, column=0, padx=10, pady=10)
        self.entry_hash = ctk.CTkEntry(self.conf, placeholder_text="test_hashes.csv")
        self.entry_hash.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        ctk.CTkButton(self.conf, text="Browse", width=60, command=self.browse_hash).grid(row=0, column=2, padx=10)

        ctk.CTkLabel(self.conf, text="Wordlist Source:").grid(row=1, column=0, padx=10, pady=10)
        self.entry_dict = ctk.CTkEntry(self.conf, placeholder_text="dictionary.txt")
        self.entry_dict.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        ctk.CTkButton(self.conf, text="Browse", width=60, command=self.browse_dict).grid(row=1, column=2, padx=10)

        self.btn_gen = ctk.CTkButton(self.conf, text="GENERATE AUDIT REPORT", fg_color="purple", hover_color="darkviolet", 
                                     font=ctk.CTkFont(weight="bold"), command=self.start_report)
        self.btn_gen.grid(row=2, column=0, columnspan=3, pady=20, sticky="ew", padx=20)

        # Preview
        self.lbl_prev = ctk.CTkLabel(self, text="Report Preview:", font=ctk.CTkFont(weight="bold"))
        self.lbl_prev.grid(row=3, column=0, sticky="nw", pady=(10,0))
        
        self.textbox = ctk.CTkTextbox(self, font=ctk.CTkFont(family="Courier", size=12))
        self.textbox.grid(row=4, column=0, sticky="nsew", pady=5)

    def browse_hash(self):
        f = ctk.filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if f: 
            self.entry_hash.delete(0, "end")
            self.entry_hash.insert(0, f)

    def browse_dict(self):
        f = ctk.filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if f: 
            self.entry_dict.delete(0, "end")
            self.entry_dict.insert(0, f)

    def start_report(self):
        hash_f = self.entry_hash.get()
        dict_f = self.entry_dict.get()
        
        if not os.path.exists(hash_f) or not os.path.exists(dict_f):
            messagebox.showerror("Error", "Please select valid files")
            return
            
        self.btn_gen.configure(state="disabled", text="Analyzing...")
        
        threading.Thread(target=self.run, args=(hash_f, dict_f)).start()

    def run(self, h, d):
        try:
            report_text, path = self.generator.generate_security_audit(h, d)
            self.after(0, lambda: self.show_report(report_text, path))
        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Error", str(e)))
        finally:
            self.after(0, lambda: self.btn_gen.configure(state="normal", text="GENERATE AUDIT REPORT"))

    def show_report(self, text, path):
        self.textbox.delete("0.0", "end")
        self.textbox.insert("0.0", text)
        messagebox.showinfo("Report Ready", f"Report saved to:\n{os.path.abspath(path)}")
