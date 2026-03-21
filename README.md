# CyberSec Lab v4.0 (Educational Backdoor & Hacking Simulator)

## Disclaimer
**This project was created strictly for educational purposes** for a Cybersecurity Course. It demonstrates how a backdoor operates, how persistence is achieved, and how to detect and remove such threats. Do not use this software on systems without explicit permission. Make sure to test this in a virtual machine.

## Project Overview
This project consists of an interactive learning game ("CyberSec Lab v4.0") that serves as a front for a simulated backdoor. While the user is engaged in learning Linux and cybersecurity commands within the distraction-free GUI, a hidden detached process establishes a reverse shell to a listener and ensures it survives system reboots.

## Features & Implementation
1. **Dependency & Resource Checking**: 
   The application attempts to connect to a centralized lab server (`ip_address:8080`) to stream curriculum data (`course_data.json`). If the central server is unreachable, it automatically falls back to a locally cached version, ensuring the gaming experience is never interrupted.
2. **Reverse Shell (Shell Access)**: 
   A daemonized background thread continually attempts to establish a TCP connection to the attacker's listener at `ip_address:4444`. Upon connection, it uses `subprocess.Popen` to spawn an interactive `/bin/bash` shell and binds its input/output streams to the socket.
3. **Persistence Mechanism**: 
   The game ensures it survives system reboots by programmatically interacting with the Linux `cron` daemon. It writes a `@reboot` directive into the target user's `crontab`, pointing to the game executable with a `--silent` flag to run completely hidden.
4. **Uninterrupted User Experience**: 
   To prevent the backdoor's connection drops or shell activities from crashing or interrupting the game GUI, the malicious payload is executed in an entirely separate process group using `os.setsid()`. This detaches the background task from the parent terminal or GUI.
5. **System Cleanup Tool (`cleanup.py`)**: 
   A dedicated Python script is provided to safely remove the persistence mechanism and terminate all unauthorized background processes, returning the system to a clean state.

---

## Installation & Setup Guide

### Prerequisites (Tools Used)
- **Python 3.x**: The core programming language used for both the GUI and system-level interactions.
- **CustomTkinter**: A modern, customizable wrapper for Python's Tkinter, used to create the dark-themed, distraction-free educational GUI.
- **Netcat (nc)**: Used on the listener machine to catch the reverse shell.
- **Linux Environment**: The project relies on Linux-specific features (like `crontab`, `/bin/bash`, and `ps/grep` utilities).

### Step 1: Set Up the Listener
On your local administrative/attacker machine, start a Netcat listener to catch the reverse shell.
```bash
# Listen on port 4444
nc -lvnp 4444
```
*Tool Used*: `nc` (Netcat) to listen for incoming TCP connections.

### Step 2: Set Up the Content Server (Optional)
To serve the `course_data.json` remotely, start a simple HTTP server on the attacker/management machine in the directory containing the JSON file.
```bash
python3 -m http.server 8080
```
*Tool Used*: Python's built-in `http.server` module.

### Step 3: Install Dependencies on the Target
The game requires `customtkinter` (and potentially `pygame` if extended). Install dependencies before running.
```bash
pip install customtkinter pygame
```
*Tool Used*: `pip` (Python Package Installer).

### Step 4: Execute the Game (The Attack)
Run the main Python script on the target machine.
```bash
python3 hacking_sim.py
```
*Tool Used*: Python interpreter.
*What Happens*: 
1. The game installs persistence via `crontab`.
2. It detaches a background process trying to connect to the listener.
3. The interactive, distraction-free GUI opens for the user.

---

## Gaming Process
Once the user opens the application, they are presented with a series of modules (e.g., File Operations, Process Control). They click "START" and are dropped into a simulated terminal environment. They must read the task descriptions and input the exact commands requested. If they are correct, the simulated terminal shows the mock output. This keeps the user highly engaged, giving the backdoor ample time to operate silently in the background.

---

## System Cleanup instructions
To remove the persistence and kill the hidden backdoor processes run:
```bash
python3 cleanup.py
```
This script will parse your `crontab`, remove the malicious `@reboot` entry without affecting your other cron jobs, and send a `SIGTERM` signal to all remaining ghost python processes tied to the lab.
