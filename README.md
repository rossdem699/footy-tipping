# Footy Tipping Assistant (AFL & NRL)

[![Latest Release](https://img.shields.io/github/v/release/rossdem699/footy-tipping?label=latest%20update)](https://github.com/rossdem699/footy-tipping/releases)

An automated tipping analysis tool that fetches odds, reviews injury updates, and recommends weekly tipping picks for AFL and NRL games.

---

## 🆕 What's New in the Latest Update

*   **Confidence Percentage (Implied Probability):** Tips now display a confidence percentage calculated and normalized from decimal bookmaker odds (e.g., `Geelong (59%)`) instead of raw decimal values, providing clearer insight into tipping strength.
*   **Shortened Team Names:** Integrated team name shortening (e.g., `Sea Eagles` vs `Rabbitohs` instead of full names) to ensure terminal tables stay narrow and do not break or wrap lines.
*   **Animated CLI Spinner Loader (`run_with_spinner.sh`):** A custom launcher wrapper featuring a bouncing rugby ball loading animation (`🏉`) to provide visual feedback during the 2-3 minute analysis process.
*   **Automatic Markdown Table Alignment (`align_markdown.py`):** Added a python script that parses and aligns markdown tables output by the tipping agent, ensuring perfectly printed columns in the terminal.
*   **Updated Procedures:** Aligned [GEMINI.md](file:///home/ross/projects/footy_tipping/GEMINI.md) guidelines with these new output standards.

---


## ⚙️ Installation & How to Run

### Local Setup
*   **Recommended Python Version:** Python 3.12
*   **How to ensure the correct Python version is used:** By using a local **Virtual Environment** (`venv`). This locks execution to the virtual environment's dedicated Python interpreter and isolates project dependencies.

1. **Navigate to the project folder:**
   ```bash
   cd /home/ross/projects/footy_tipping
   ```
2. **Setup the Virtual Environment:**
   Initialize the environment using your system Python 3.12:
   ```bash
   python3 -m venv venv
   ```
3. **Activate the Environment:**
   ```bash
   source venv/bin/activate
   ```
4. **Install Dependencies (using the requirements file):**
   ```bash
   pip install -r requirements.txt
   ```

### Execution
*   **Desktop Launcher (Easiest):**
    Double-click the **Footy YOLO** shortcut on your desktop. It will automatically run the Antigravity CLI (`agy`) headlessly, query current tipping info using our procedure guidelines, display the results in a terminal window, and pause for you to press Enter before closing.
*   **Manual CLI Command:**
    To run the analysis manually via the terminal, use the Antigravity CLI:
    ```bash
    /home/ross/.local/bin/agy -p 'Get footy tips for the next round following the procedure in GEMINI.md. Do not use python; use your research tools to fetch live odds and news. Produce narrow markdown tables with a separate reasoning list below them.' --dangerously-skip-permissions
    ```

---

## 🏉 Key Files

*   [GEMINI.md](file:///home/ross/projects/footy_tipping/GEMINI.md): Core tipping guidelines, rules, and layout instructions used by the agent to structure the output.
*   `src/`: Python source scripts for automation and Playwright/Ollama LLM integrations.
*   `tip_history.json`: Historical log of tip performance, odds tracker, and round results.
*   `setup_desktop.sh`: Utility script that creates and updates the desktop shortcut.
*   `run_with_spinner.sh`: Bash launcher wrapper that runs the agent with a bouncing rugby ball loading animation.
*   `align_markdown.py`: Utility python script to parse and align table column widths in the terminal.
