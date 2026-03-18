import os
import sys

def remove_persistence():
    print("[*] Starting Cleanup...")
    if sys.platform == "win32":
        import winreg
        try:
            key = winreg.HKEY_CURRENT_USER
            key_value = "Software\\Microsoft\\Windows\\CurrentVersion\\Run"
            open_key = winreg.OpenKey(key, key_value, 0, winreg.KEY_ALL_ACCESS)
            winreg.DeleteValue(open_key, "RCABackdoorGame")
            winreg.CloseKey(open_key)
            print("[+] Windows Registry entry removed.")
        except Exception as e:
            print("[-] Persistence entry not found.")

if __name__ == "__main__":
    remove_persistence()
    
    # Remove downloaded dependency
    if os.path.exists("assets_lib.txt"):
        os.remove("assets_lib.txt")
        print("[+] Temporary dependencies deleted.")
        
    print("\n[SUCCESS] System is now clean.")
    input("Press Enter to exit...")