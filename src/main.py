import os
import json
import logging
import urllib.request
import time
import subprocess
import webbrowser
import sys
import argparse
from datetime import datetime
from typing import List, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- CONFIGURATION ---
def load_env():
    env_vars = {}
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    env_vars[key] = value
    return env_vars

ENV = load_env()
API_KEY = ENV.get('ODDS_API_KEY', '06366847d51a2cd764e4cb560d62be53')
HISTORY_FILE = 'tip_history.json'

SPORTS = {
    'rugbyleague_nrl': 'NRL',
    'aussierules_afl': 'AFL'
}

BOOKMAKERS_TO_CHECK = ['sportsbet', 'tab', 'ladbrokes', 'neds']

SHORT_NAMES = {
    # NRL
    "Brisbane Broncos": "Broncos",
    "Canterbury Bulldogs": "Bulldogs",
    "North Queensland Cowboys": "Cowboys",
    "St George Illawarra Dragons": "Dragons",
    "Parramatta Eels": "Eels",
    "Newcastle Knights": "Knights",
    "Penrith Panthers": "Panthers",
    "South Sydney Rabbitohs": "Rabbitohs",
    "Canberra Raiders": "Raiders",
    "Sydney Roosters": "Roosters",
    "Manly Warringah Sea Eagles": "Sea Eagles",
    "Cronulla Sutherland Sharks": "Sharks",
    "Melbourne Storm": "Storm",
    "Wests Tigers": "Tigers",
    "New Zealand Warriors": "Warriors",
    "Gold Coast Titans": "Titans",
    "Dolphins": "Dolphins",
    # AFL
    "Adelaide Crows": "Crows",
    "Brisbane Lions": "Lions",
    "Carlton Blues": "Blues",
    "Collingwood Magpies": "Magpies",
    "Essendon Bombers": "Bombers",
    "Fremantle Dockers": "Dockers",
    "Geelong Cats": "Cats",
    "Gold Coast Suns": "Suns",
    "GWS Giants": "Giants",
    "Greater Western Sydney Giants": "Giants",
    "Hawthorn Hawks": "Hawks",
    "Melbourne Demons": "Demons",
    "North Melbourne Kangaroos": "Kangaroos",
    "Port Adelaide Power": "Power",
    "Richmond Tigers": "Tigers",
    "St Kilda Saints": "Saints",
    "Sydney Swans": "Swans",
    "West Coast Eagles": "Eagles",
    "Western Bulldogs": "Bulldogs"
}

def shorten_team(name: str) -> str:
    return SHORT_NAMES.get(name.strip(), name)

# --- CORE FUNCTIONS ---

def fetch_odds(sport_key: str) -> List[Dict[str, Any]]:
    url = f"https://api.the-odds-api.com/v4/sports/{sport_key}/odds/?api_key={API_KEY}&regions=au&markets=h2h&oddsFormat=decimal"
    try:
        with urllib.request.urlopen(url) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        logging.error(f"Failed to fetch {sport_key}: {e}")
        return []

def calculate_tips(games: List[Dict[str, Any]]) -> Dict[str, Any]:
    results = {}
    for game in games:
        home_team = game['home_team']
        away_team = game['away_team']
        game_id = game['id']
        commence_time = datetime.fromisoformat(game['commence_time'].replace('Z', '+00:00'))
        
        odds_pool = {home_team: [], away_team: []}
        for bookmaker in game.get('bookmakers', []):
            if bookmaker['key'] in BOOKMAKERS_TO_CHECK:
                for market in bookmaker.get('markets', []):
                    if market['key'] == 'h2h':
                        for outcome in market['outcomes']:
                            odds_pool[outcome['name']].append(outcome['price'])
        
        avg_home = sum(odds_pool[home_team]) / len(odds_pool[home_team]) if odds_pool[home_team] else 0
        avg_away = sum(odds_pool[away_team]) / len(odds_pool[away_team]) if odds_pool[away_team] else 0
        
        # Calculate implied probabilities and confidence percentage
        p_home = 1.0 / avg_home if avg_home > 0 else 0
        p_away = 1.0 / avg_away if avg_away > 0 else 0
        p_sum = p_home + p_away
        
        if p_sum > 0:
            prob_home = p_home / p_sum
            prob_away = p_away / p_sum
        else:
            prob_home = 0.5
            prob_away = 0.5
            
        if avg_home > 0 and (avg_away == 0 or avg_home < avg_away):
            tip = home_team
            confidence_pct = round(prob_home * 100)
        elif avg_away > 0:
            tip = away_team
            confidence_pct = round(prob_away * 100)
        else:
            tip = "Unknown"
            confidence_pct = 50
            
        results[game_id] = {
            "game": f"{home_team} vs {away_team}",
            "time": commence_time.strftime("%d %b, %H:%M"),
            "tip": tip,
            "odds": f"H:{avg_home:.2f} | A:{avg_away:.2f}",
            "confidence": f"{confidence_pct}%"
        }
    return results

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_history(history):
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=4)

def generate_report(current_tips, history):
    report = f"\nFOOTY TIPPING BOT REPORT - {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
    
    for sport_key, sport_name in SPORTS.items():
        sport_tips = current_tips.get(sport_key, {})
        
        if not sport_tips:
            report += f"\n--- {sport_name} ---\nNo upcoming games found.\n"
            continue

        headers = ["Kickoff", "Match", "Recommended Tip", "Confidence"]
        rows = []
        for game_id, data in sport_tips.items():
            old_data = history.get(sport_key, {}).get(game_id)
            change_marker = ""
            if old_data and old_data['tip'] != data['tip']:
                change_marker = " ⚠️ [CHANGED]"
            
            # Shorten team names for a neat terminal table
            if " vs " in data['game']:
                home, away = data['game'].split(" vs ", 1)
                match_name = f"{shorten_team(home)} vs {shorten_team(away)}"
            else:
                match_name = data['game']
            
            rows.append([
                data['time'],
                match_name,
                f"{shorten_team(data['tip'])}{change_marker}",
                data.get('confidence', data.get('odds', ''))
            ])

        # Determine column widths for alignment
        col_widths = [len(h) for h in headers]
        for row in rows:
            for i, val in enumerate(row):
                col_widths[i] = max(col_widths[i], len(val))

        # Dynamic separator width
        table_width = sum(col_widths) + 3 * len(headers) + 1
        
        report += f"\n--- {sport_name} ---\n"
        report += "=" * table_width + "\n"
        
        # Build table
        header_line = "| " + " | ".join(f"{h:<{col_widths[i]}}" for i, h in enumerate(headers)) + " |"
        separator_line = "| " + " | ".join("-" * col_widths[i] for i in range(len(headers))) + " |"
        
        report += header_line + "\n"
        report += separator_line + "\n"
        for row in rows:
            row_line = "| " + " | ".join(f"{val:<{col_widths[i]}}" for i, val in enumerate(row)) + " |"
            report += row_line + "\n"
            
        report += "=" * table_width + "\n"
        
    return report

def main():
    parser = argparse.ArgumentParser(description='Footy Tipping Bot')
    parser.add_argument('--headless', action='store_true', help='Run browser in headless mode')
    parser.add_argument('--yolo', action='store_true', help='Bypass confirmation prompt')
    args = parser.parse_args()

    current_all_tips = {}
    history = load_history()

    for sport_key in SPORTS:
        raw_data = fetch_odds(sport_key)
        current_all_tips[sport_key] = calculate_tips(raw_data)

    report = generate_report(current_all_tips, history)
    print(report)
    
    # Save current tips for next time
    save_history(current_all_tips)
    
    # Save report to text file
    with open('latest_tips.txt', 'w') as f:
        f.write(report)
    
    print("\n" + "="*50)
    print("READY FOR AUTOMATIC TIPPING")
    print("="*50)
    
    if args.yolo:
        choice = 'y'
        print("\n[YOLO MODE] Bypassing confirmation...")
    else:
        choice = input("\nWould you like to AUTOMATICALLY place these tips on ESPN now? (y/n): ")
    
    if choice.lower() == 'y':
        print("\n" + "="*50)
        print("BOT TRIGGERED: Starting the Playwright Auto-Tipper...")
        print("========================================")
        
        try:
            import auto_tip_playwright
            nrl_tips = current_all_tips.get('rugbyleague_nrl', {})
            afl_tips = current_all_tips.get('aussierules_afl', {})
            
            if not args.headless:
                print("\n[!] A new browser window will open.")
                print("[!] PLEASE LOG IN MANUALLY if the bot doesn't do it automatically.")
                print("[!] Once you reach your tipping dashboard, the robot will take over.")
            
            auto_tip_playwright.run_tipping(nrl_tips, afl_tips, headless=args.headless)
            print("\n[SUCCESS] Tipping process finished!")
        except ImportError:
            print("\n[!] ERROR: Playwright is not installed.")
            print("Please run these commands in your terminal first:")
            print("  python3 -m pip install playwright")
            print("  python3 -m playwright install chromium")
        except Exception as e:
            print(f"\n[ERROR] The Auto-Tipper failed: {e}")
    
    if not args.yolo:
        input("\nBot process finished. Press ENTER to close...")
    else:
        print("\nBot process finished.")

if __name__ == "__main__":
    main()

