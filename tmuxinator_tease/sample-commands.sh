#!/bin/bash

SESSION="sample"

# Window 1 (editor) - index 1
tmux send-keys -t $SESSION:1.1 'vim' C-m
tmux send-keys -t $SESSION:1.2 'htop' C-m

# Window 2 (server) - index 2
tmux send-keys -t $SESSION:2.1 'htop' C-m

# Window 3 (logs) - index 3
tmux send-keys -t $SESSION:3.1 'htop' C-m

# Window 4 (xyz) - index 4
tmux send-keys -t $SESSION:4.1 'sleep 5 && date' C-m
