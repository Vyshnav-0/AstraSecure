import customtkinter as ctk
from modules.bruteforce_simulator import BruteForceSimulator
import threading
import tkinter.messagebox as messagebox

class BruteForcePage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        
        self.simulator = BruteForceSimulator()
        self.attack_thread = None

        # Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Header
        self.header = ctk.CTkFrame(self, fg_color="transparent")
        self.header.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        ctk.CTkLabel(self.header, text="Brute-Force Simulator", font=("Roboto", 28, "bold")).pack(side="left")
        ctk.CTkLabel(self.header, text=" CPU-intensive cracking demo.", text_color="gray70", font=("Roboto", 14)).pack(side="left", padx=10, pady=(10, 0))

        # --- Settings Card ---
        self.card_conf = ctk.CTkFrame(self, fg_color="#2b2b2b", corner_radius=15)
        self.card_conf.grid(row=1, column=0, sticky="ew", padx=0, pady=10)
        self.card_conf.grid_columnconfigure(1, weight=1)

        # Row 1: Target & Algo
        ctk.CTkLabel(self.card_conf, text="Target Hash:", font=("Roboto", 14, "bold")).grid(row=0, column=0, sticky="w", padx=20, pady=20)
        self.entry_hash = ctk.CTkEntry(self.card_conf, placeholder_text="Paste target hash...", height=40)
        self.entry_hash.grid(row=0, column=1, sticky="ew", padx=10)
        
        self.combo_algo = ctk.CTkComboBox(self.card_conf, values=["MD5", "SHA256", "SHA512"], width=100)
        self.combo_algo.grid(row=0, column=2, padx=20)
        self.combo_algo.set("SHA256")

        # Row 2: Charset
        self.frame_opts = ctk.CTkFrame(self.card_conf, fg_color="transparent")
        self.frame_opts.grid(row=1, column=0, columnspan=3, sticky="w", padx=10, pady=(0, 20))
        
        self.var_lower = ctk.BooleanVar(value=True)
        self.var_upper = ctk.BooleanVar()
        self.var_nums = ctk.BooleanVar()
        self.var_syms = ctk.BooleanVar()
        
        ctk.CTkLabel(self.frame_opts, text="Charset:", text_color="gray").pack(side="left", padx=10)
        ctk.CTkCheckBox(self.frame_opts, text="a-z", variable=self.var_lower).pack(side="left", padx=10)
        ctk.CTkCheckBox(self.frame_opts, text="A-Z", variable=self.var_upper).pack(side="left", padx=10)
        ctk.CTkCheckBox(self.frame_opts, text="0-9", variable=self.var_nums).pack(side="left", padx=10)
        ctk.CTkCheckBox(self.frame_opts, text="Symbols", variable=self.var_syms).pack(side="left", padx=10)

        ctk.CTkLabel(self.frame_opts, text="|   Max Length:", text_color="gray").pack(side="left", padx=20)
        self.slider_len = ctk.CTkSlider(self.frame_opts, from_=1, to=8, number_of_steps=7, width=150)
        self.slider_len.set(4)
        self.slider_len.pack(side="left", padx=5)
        self.lbl_len_val = ctk.CTkLabel(self.frame_opts, text="4", font=("Roboto", 14, "bold"))
        self.lbl_len_val.pack(side="left", padx=5)
        
        self.slider_len.configure(command=lambda v: self.lbl_len_val.configure(text=str(int(v))))

        # Action Btn
        self.btn_start = ctk.CTkButton(self.card_conf, text="START ATTACK", command=self.start_attack, 
                                       height=50, fg_color="#c62828", hover_color="#8e0000", font=("Roboto", 16, "bold"))
        self.btn_start.grid(row=2, column=0, columnspan=3, padx=20, pady=(0, 20), sticky="ew")

        # --- Monitor / Terminal ---
        self.card_term = ctk.CTkFrame(self, fg_color="#1a1a1a", corner_radius=15, border_width=1, border_color="#333")
        self.card_term.grid(row=2, column=0, sticky="nsew", padx=0, pady=10)
        self.card_term.grid_columnconfigure(0, weight=1)
        self.card_term.grid_rowconfigure(2, weight=1)

        self.lbl_status = ctk.CTkLabel(self.card_term, text="READY TO ATTACK", font=("Consolas", 18, "bold"), text_color="#c62828")
        self.lbl_status.grid(row=0, column=0, pady=(20, 5))
        
        self.lbl_stats = ctk.CTkLabel(self.card_term, text="0 Attempts | Speed: 0 H/s", font=("Consolas", 14), text_color="gray")
        self.lbl_stats.grid(row=1, column=0, pady=(0, 10))

        self.console = ctk.CTkTextbox(self.card_term, font=("Consolas", 12), fg_color="transparent", text_color="#00ff00")
        self.console.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)
        
        # Stop btn (Hidden initially)
        self.btn_stop = ctk.CTkButton(self.card_term, text="STOP", width=100, height=30, fg_color="gray", command=self.stop_attack)

    def log(self, text):
        self.console.insert("end", text + "\n")
        self.console.see("end")

    def toggle_ui(self, running):
        state = "disabled" if running else "normal"
        self.entry_hash.configure(state=state)
        # We don't disable start button, we hide it or swap it ideally.
        if running:
            self.btn_start.configure(state="disabled", text="ATTACK IN PROGRESS...")
            self.btn_stop.grid(row=0, column=0, sticky="e", padx=20, pady=20) # Overlay stop button top right
        else:
            self.btn_start.configure(state="normal", text="START ATTACK")
            self.btn_stop.grid_forget()

    def update_status_callback(self, current_guess, attempts, speed):
        self.after(0, lambda: self._update_labels(current_guess, attempts, speed))

    def _update_labels(self, guess, attempts, speed):
        self.lbl_status.configure(text=f"TRYING: {guess}")
        self.lbl_stats.configure(text=f"{attempts:,} Attempts | {int(speed):,} H/s")

    def success_callback(self, result, attempts, time_taken):
        self.after(0, lambda: self._handle_result(result, attempts, time_taken))

    def _handle_result(self, result, attempts, time_taken):
        self.toggle_ui(False)
        self.lbl_stats.configure(text=f"Total: {attempts:,} Attempts | Time: {time_taken:.2f}s")
        
        if result:
            self.lbl_status.configure(text=f"CRACKED: {result}", text_color="#00ff00")
            self.log(f"[+] FOUND: {result}")
            messagebox.showinfo("Success", f"Password Found: {result}")
        else:
            self.lbl_status.configure(text="FAILED / STOPPED", text_color="red")
            self.log("[-] Not found.")

    def start_attack(self):
        target = self.entry_hash.get().strip()
        if not target: return
        
        algo = self.combo_algo.get()
        charset = self.simulator.get_charset(self.var_lower.get(), self.var_upper.get(), self.var_nums.get(), self.var_syms.get())
        if not charset: return
        max_len = int(self.slider_len.get())
        
        self.toggle_ui(True)
        self.console.delete("0.0", "end")
        self.log(f"[*] Starting {algo} attack on {target}...")
        
        self.attack_thread = threading.Thread(
            target=self.simulator.attack,
            args=(target, algo, charset, max_len, self.update_status_callback, self.success_callback),
            daemon=True
        )
        self.attack_thread.start()

    def stop_attack(self):
        if self.simulator.running:
            self.simulator.stop()
