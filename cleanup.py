import subprocess
import os

def surgical_cleanup():
    print("[*] Initiating targeted teardown...")

    # 1. Targeted Process Kill
    # This specifically kills the --silent background instance
    try:
        subprocess.run(["pkill", "-9", "-f", "hacking_sim.py --silent"], check=True)
        print("[+] Terminated: Background lab process.")
    except subprocess.CalledProcessError:
        print("[!] No active background lab process found.")

    # 2. Targeted Crontab Removal
    # This filters out ONLY the line containing 'hacking_sim.py'
    # It preserves all other crontab entries.
    try:
        # Get existing crontab
        current_cron = subprocess.check_output("crontab -l", shell=True, stderr=subprocess.DEVNULL).decode()
        
        # Filter the lines
        new_cron = "\n".join([line for line in current_cron.splitlines() if "hacking_sim.py" not in line])
        
        # Write the filtered crontab back
        if new_cron.strip():
            process = subprocess.Popen(['crontab', '-'], stdin=subprocess.PIPE)
            process.communicate(input=new_cron.encode())
        else:
            # If no lines remain, just remove the crontab
            subprocess.run(["crontab", "-r"], check=True)
            
        print("[+] Removed: 'hacking_sim.py' from crontab.")
    except Exception as e:
        print("[-] Crontab was already clean or does not exist.")

    print("[*] Teardown complete.")

if __name__ == "__main__":
    surgical_cleanup()