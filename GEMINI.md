# Weekly Tipping Procedure (NRL & AFL)

Whenever the user asks for "tips" or "tipping analysis", follow these steps for **NRL and AFL only**:

1. **Verify Round Status:** Check the current round status for both NRL and AFL (e.g., split rounds, Las Vegas, Opening Round, or Gather Round).
    - **STRICT EXCLUSION:** Do not include Super League, international fixtures, or other codes, even if they are part of a shared event (e.g., Las Vegas).
    - Do not jump to the next full round unless the current round is >90% complete.
2. **Get Odds Data:** Run `python3 src/tipping_engine.py` (if available) or use `google_web_search` to find live odds for NRL and AFL from Sportsbet, TAB, or Ladbrokes.
3. **Analyze Shifts:** Note any "TIP CHANGE" or "ODDS SHIFT" compared to previous data in `tip_history.json`.
4. **Research News:** Perform a `google_web_search` for:
    - "NRL Round [Current] late mail injury news"
    - "AFL Round [Current] late mail injury news"
5. **Final Recommendation:** Provide separate, clean, and terminal-friendly tables for **AFL first**, then **NRL**, using a narrow table layout with a separate reasoning section to prevent horizontal wrapping.
    - **Use Short Team Names:** Use shortened team names in the table (e.g., "Sea Eagles vs Rabbitohs", "Geelong", "Storm", "Roosters") rather than full names to keep the table narrow and prevent terminal line wrapping.
    - **Confidence Percentage in Tip Column:** Instead of listing the actual odds value (e.g., $1.60), list the confidence percentage in the tip (e.g., Geelong (59%)). Calculate this confidence percentage from the decimal odds (normalized to sum to 100%): e.g. for odds 1.60 vs 2.30, the implied probabilities are 1/1.60 = 62.5% and 1/2.30 = 43.5%, normalized to 59% confidence for Geelong.
    - Format exactly like this:

   **[League Name] - Round [Number] Tips**
   | Match | Tip & Odds | Kickoff | Confidence |
   | :--- | :--- | :--- | :--- |
   | [Short Team A] vs [Short Team B] | [Short Recommended Team] ([Confidence Percentage]%) | [Time until kickoff in Days and Hours] | [High/Med/Low] |

   **Reasoning & Match Notes:**
   - **[Short Team A] vs [Short Team B]**: [Details including injury returns, market moves, etc.]

   - **Completed Games:** For games that have already finished in the current round, list them in the table too, showing the actual winner/result in the "Tip & Odds" column (e.g., "Won 84-60" or "Lost 12-18") and highlight upsets (e.g., using **⚠️ UPSET** in the match name or result).
   - **Highlighting:** Use emojis and bold text for key player updates or major market pivots in the reasoning list.

## Tipping Logic:
- **Primary:** Betting Odds (The market is usually correct).
- **Secondary:** Key Players/Injuries (Can override odds if the shift is significant).
- **Tertiary:** Ladder Position (Used for tie-breakers).
- **Context:** If odds have moved significantly (e.g., $1.50 -> $1.80), investigate why!

