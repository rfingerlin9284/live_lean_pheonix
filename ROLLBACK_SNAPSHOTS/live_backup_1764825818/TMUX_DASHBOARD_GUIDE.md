# RICK PHOENIX: System Dashboard

## Status: ACTIVE 🟢
The system is currently running in a 4-pane TMUX session (`RICK_PHOENIX`).

## Navigation Controls (Laptop Friendly)
- **Shift + Arrow Keys**: Move focus between panes.
- **Alt + Arrow Keys**: Alternative movement.
- **Ctrl + Arrow Keys**: Alternative movement.
- **Alt + Click**: Select a pane with the mouse.

## Session Management
- **Detach (Keep running in background)**: Press `Ctrl+b` then `d`.
- **Re-attach**: Run `tmux attach -t RICK_PHOENIX`.
- **Kill/Stop**: Run the "Safe Shutdown" task or `tmux kill-session -t RICK_PHOENIX`.

## Panes
1. **Top Left**: `oanda_trading_engine.py` (The Brain)
2. **Top Right**: `rick_narrator.py` (The Voice)
3. **Bottom Left**: `market_scanner.py` (The Eyes)
4. **Bottom Right**: `system_monitor.py` (The Pulse)
