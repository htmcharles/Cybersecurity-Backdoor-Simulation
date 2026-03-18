
# Project: Educational Trojan Game (RCA Cybersecurity)
**Date:** March 18, 2026

## Features Mapping (50 Points)
1. **Dependency Installation (5pts):** `main_game.py` uses `requests` to pull `assets_lib.txt` from a local server.
2. **Shell Access (10pts):** `communication.py` provides a reverse shell to `listener.py`.
3. **No Interruption (10pts):** `threading` module keeps the game GUI responsive while the shell works.
4. **Persistence (5pts):** Adds the game to `HKEY_CURRENT_USER\...\Run` in the Windows Registry.
5. **Cleanup (5pts):** `cleanup.py` removes the registry key and downloaded assets.
6. **Notification (5pts):** A `messagebox` alerts the user before the game starts.
7. **Documentation (5pts):** This Readme and technical comments in code.
8. **Innovation (5pts):** Integrated **Security Awareness HUD** that displays defense tips while playing.

## How to Test
1. Attacker: Run `python listener.py`.
 pyinstaller --onefile --noconsole main_game.py
2. Attacker: Run `python -m http.server 8080` (to host dependency file).
3. Target: Run `python main_game.py`.
4. Result: Control the target shell while playing the game.