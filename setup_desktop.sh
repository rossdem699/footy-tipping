#!/bin/bash

YOLO_FILE="$HOME/Desktop/FootyYolo.desktop"

# Create Footy YOLO Shortcut for Antigravity CLI (agy)
# Note: -p flag triggers headless mode.
# --dangerously-skip-permissions bypasses all confirmation questions.
cat <<EOF > "$YOLO_FILE"
[Desktop Entry]
Version=1.0
Name=Footy YOLO
Comment=Get Footy Tips via Antigravity CLI (Headless)
Exec=bash -c "/home/ross/projects/footy_tipping/run_with_spinner.sh && read -p 'Press enter to close...' "
Path=/home/ross/projects/footy_tipping
Icon=football
Terminal=true
Type=Application
Categories=Application;
EOF

chmod +x "$YOLO_FILE"

echo "=================================================="
echo "SUCCESS: Footy YOLO Antigravity CLI Shortcut Created!"
echo "- Action: Runs Antigravity CLI (agy) in Headless/YOLO mode"
echo "- Logic: Uses GEMINI.md instructions"
echo "- Icon: Football"
echo "=================================================="
