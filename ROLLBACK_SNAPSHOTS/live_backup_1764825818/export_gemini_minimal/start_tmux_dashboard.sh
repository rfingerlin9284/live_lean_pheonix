#!/bin/bash
SESSION="RICK_PHOENIX"

# Force Python to flush stdout/stderr immediately
export PYTHONUNBUFFERED=1

# Check if session exists
tmux has-session -t $SESSION 2>/dev/null

if [ $? != 0 ]; then
  # Create new session
  tmux new-session -d -s $SESSION

  # Rename window
  tmux rename-window -t $SESSION:0 'RICK_DASHBOARD'
  
  # Split horizontally (Left | Right)
  # Result: Pane 0 (Left), Pane 1 (Right)
  tmux split-window -h
  
  # Split Left pane vertically (Top Left | Bottom Left)
  # Result: Pane 0 (Top Left), Pane 1 (Bottom Left), Pane 2 (Right)
  tmux select-pane -t 0
  tmux split-window -v
  
  # Split Right pane vertically (Top Right | Bottom Right)
  # Result: Pane 0 (TL), Pane 1 (BL), Pane 2 (TR), Pane 3 (BR)
  tmux select-pane -t 2
  tmux split-window -v
  
  # ---------------------------------------------------------
  # Pane 0: Top Left -> The Brain (Engine)
  # ---------------------------------------------------------
  tmux select-pane -t 0
  tmux send-keys "echo '🧠 STARTING THE BRAIN (Engine)...'" C-m
  tmux send-keys "./start_with_integrity.sh" C-m
  
  # ---------------------------------------------------------
  # Pane 1: Bottom Left -> The Eyes (Sentinel)
  # ---------------------------------------------------------
  tmux select-pane -t 1
  tmux send-keys "echo '🛡️ STARTING THE EYES (Sentinel)...'" C-m
  tmux send-keys "python3 active_trade_monitor.py" C-m
  
  # ---------------------------------------------------------
  # Pane 2: Top Right -> The Voice (Narrator)
  # ---------------------------------------------------------
  tmux select-pane -t 2
  tmux send-keys "echo '🗣️ STARTING THE VOICE (Narrator)...'" C-m
  tmux send-keys "tail -f narration.jsonl | python3 pretty_print_narration.py" C-m
  
  # ---------------------------------------------------------
  # Pane 3: Bottom Right -> The Pulse (Watchdog)
  # ---------------------------------------------------------
  tmux select-pane -t 3
  tmux send-keys "echo '💓 STARTING THE PULSE (Watchdog)...'" C-m
  tmux send-keys "python3 system_watchdog.py" C-m
  
  # Select the Brain pane as active
  tmux select-pane -t 0
fi

# ---------------------------------------------------------
# Configuration (Applied every time)
# ---------------------------------------------------------
# 1. Enable Mouse (Try holding ALT while clicking if normal click fails)
tmux set-option -g mouse on

# 2. Keyboard Navigation: MULTIPLE OPTIONS
# Option A: Alt + Arrow Keys
tmux bind-key -n M-Left select-pane -L
tmux bind-key -n M-Right select-pane -R
tmux bind-key -n M-Up select-pane -U
tmux bind-key -n M-Down select-pane -D

# Option B: Shift + Arrow Keys
tmux bind-key -n S-Left select-pane -L
tmux bind-key -n S-Right select-pane -R
tmux bind-key -n S-Up select-pane -U
tmux bind-key -n S-Down select-pane -D

# Option C: Ctrl + Arrow Keys
tmux bind-key -n C-Left select-pane -L
tmux bind-key -n C-Right select-pane -R
tmux bind-key -n C-Up select-pane -U
tmux bind-key -n C-Down select-pane -D

# Status Bar Styling
tmux set-option -t $SESSION status-bg green
tmux set-option -t $SESSION status-fg black
tmux set-option -t $SESSION status-interval 5
tmux set-option -t $SESSION status-left-length 30
tmux set-option -t $SESSION status-left ' 🦅 RICK PHOENIX '
tmux set-option -t $SESSION status-right ' ⌨️  Use Shift/Alt/Ctrl + Arrows | 🖱️ Try Alt+Click | ❌ Detach: Ctrl-b + d '

# Attach to session
tmux attach-session -t $SESSION
