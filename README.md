# Footy Tipping Assistant (AFL & NRL)

An automated tipping analysis tool that fetches odds, reviews injury updates, and recommends weekly tipping picks for AFL and NRL games.

---

## ⚙️ Installation & How to Run

### Local Setup
1. **Navigate to the project folder:**
   ```bash
   cd /home/ross/projects/footy_tipping
   ```
2. **Setup the Virtual Environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Install Dependencies:**
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
