#!/usr/bin/env bash

# File paths
OUTPUT_FILE="/tmp/footy_yolo_output.txt"
rm -f "$OUTPUT_FILE"

echo -e "\e[1;36m==================================================\e[0m"
echo -e "\e[1;33m       STARTING FOOTY YOLO TIPPING AGENT         \e[0m"
echo -e "\e[1;36m==================================================\e[0m"
echo -e "\e[32m- Running live web research on odds, news & injuries..."
echo -e "- This usually takes 2-3 minutes. Please wait.\e[0m\n"

# Start the agent in the background
/home/ross/.local/bin/agy -p 'Get footy tips for the next round following the procedure in GEMINI.md. Do not use python; use your research tools to fetch live odds and news. Produce narrow markdown tables with a separate reasoning list below them.' --dangerously-skip-permissions > "$OUTPUT_FILE" 2>&1 &

PID=$!

# Bouncing football frames (moving back and forth)
frames=(
  "🏉           "
  " 🏉          "
  "  🏉         "
  "   🏉        "
  "    🏉       "
  "     🏉      "
  "      🏉     "
  "       🏉    "
  "        🏉   "
  "         🏉  "
  "          🏉 "
  "           🏉"
  "          🏉 "
  "         🏉  "
  "        🏉   "
  "       🏉    "
  "      🏉     "
  "     🏉      "
  "    🏉       "
  "   🏉        "
  "  🏉         "
  " 🏉          "
)

i=0
# Disable cursor
tput civis

while kill -0 $PID 2>/dev/null; do
  frame="${frames[i]}"
  echo -ne "\r\e[1;33m[WORKING]\e[0m |$frame| Searching and analyzing... "
  i=$(( (i + 1) % ${#frames[@]} ))
  sleep 0.15
done

# Restore cursor
tput cnorm
echo -ne "\r\e[32m[DONE] Tipping analysis completed!                  \e[0m\n\n"

# Print aligned output
/home/ross/projects/footy_tipping/align_markdown.py "$OUTPUT_FILE" > "/tmp/aligned_output.txt"
mv "/tmp/aligned_output.txt" "$OUTPUT_FILE"
cat "$OUTPUT_FILE"
