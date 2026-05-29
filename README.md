# Footy Tipping Assistant (AFL & NRL)

An automated tipping analysis tool that fetches odds, reviews injury updates, and recommends weekly tipping picks for AFL and NRL games.

## Features
- **Odds Analysis:** Scrapes and tracks odds shifts from major bookmakers (TAB, Sportsbet, Ladbrokes).
- **Injury & News Research:** Fetches the latest late-mail news for key player inclusions and exclusions.
- **Form & Ladder Verification:** Uses team standings for logical tie-breakers.
- **Automated Execution:** Launches via the **Footy YOLO** desktop shortcut executing through the `agy` CLI in headless mode.

## Key Files
- [GEMINI.md](file:///home/ross/projects/footy_tipping/GEMINI.md): Core tipping guidelines and format instructions.
- `src/`: Python source scripts for automation and LLM pipelines.
- `tip_history.json`: Historical log of tip performance and round results.
