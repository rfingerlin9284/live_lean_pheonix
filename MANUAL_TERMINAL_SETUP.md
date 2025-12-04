# 🚀 RICK PHOENIX: Manual Terminal Setup

To run the system in "Persistent Terminal Mode" (without TMUX), open **4 separate terminals** in VS Code and run the following commands in each one.

### 🖥️ Terminal 1: The Engine (Core)
This runs the main trading logic. It must stay open.
```bash
./start_with_integrity.sh
```

### 🛡️ Terminal 2: System Watchdog
Monitors the health of the engine and configuration.
```bash
python3 system_watchdog.py
```
*(Now scans every 30 seconds)*

### 🎮 Terminal 3: Control Center
Your interactive menu to manage the bot.
```bash
python3 controller/main_menu.py
```

### 🗣️ Terminal 4: The Voice (Narration)
Live stream of RICK's inner monologue and decisions.
```bash
tail -f narration.jsonl | python3 pretty_print_narration.py
```

---
**Note:** To stop the system, press `Ctrl+C` in Terminal 1 (Engine). The other terminals can be closed or left open.
