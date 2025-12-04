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
  tmux split-window -h

  # ---------------------------------------------------------
  # Pane 0: Left -> The Brain/Hive/Agent (with narration)
  # ---------------------------------------------------------
  tmux select-pane -t 0
  tmux send-keys "echo '🧠 STARTING THE BRAIN/HIVE/AGENT (with narration)...'" C-m
  tmux send-keys "./start_with_integrity.sh" C-m

  # ---------------------------------------------------------
  # Pane 1: Right -> Sentinel+Watchdog (with fallback)
  # ---------------------------------------------------------
  tmux select-pane -t 1
  tmux send-keys "echo '🛡️💓 STARTING SENTINEL+WATCHDOG (with fallback)...'" C-m
  tmux send-keys "python3 active_trade_monitor.py | tee /tmp/sentinel.log & python3 system_watchdog.py | tee /tmp/watchdog.log" C-m

  # Select the Brain/Hive/Agent pane as active
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
