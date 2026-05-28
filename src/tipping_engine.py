import os
import json
import urllib.request
from datetime import datetime

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

def fetch_odds(sport_key):
    url = f"https://api.the-odds-api.com/v4/sports/{sport_key}/odds/?api_key={API_KEY}&regions=au&markets=h2h&oddsFormat=decimal"
    try:
        with urllib.request.urlopen(url) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        return []

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_history(history):
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=4)

def run_analysis():
    history = load_history()
    new_data = {}
    shifts = []

    for sport_key, sport_name in SPORTS.items():
        raw_games = fetch_odds(sport_key)
        new_data[sport_key] = {}
        
        for game in raw_games:
            game_id = game['id']
            home = game['home_team']
            away = game['away_team']
            
            # Calculate average odds
            odds_pool = {home: [], away: []}
            for bookmaker in game.get('bookmakers', []):
                if bookmaker['key'] in BOOKMAKERS_TO_CHECK:
                    for market in bookmaker.get('markets', []):
                        if market['key'] == 'h2h':
                            for outcome in market['outcomes']:
                                odds_pool[outcome['name']].append(outcome['price'])
            
            avg_home = sum(odds_pool[home]) / len(odds_pool[home]) if odds_pool[home] else 0
            avg_away = sum(odds_pool[away]) / len(odds_pool[away]) if odds_pool[away] else 0
            
            current_tip = home if (avg_home > 0 and (avg_away == 0 or avg_home < avg_away)) else away
            
            # Check for shifts
            old_game = history.get(sport_key, {}).get(game_id)
            if old_game:
                # Basic shift check: did the tip change?
                if old_game['tip'] != current_tip:
                    shifts.append(f"[TIP CHANGE] {home} vs {away}: {old_game['tip']} -> {current_tip}")
                
                # Check for significant odds movement (> 0.20)
                # Parse "H:1.37 | A:3.09" format
                try:
                    old_h = float(old_game['odds'].split('|')[0].replace('H:', '').strip())
                    if abs(avg_home - old_h) > 0.20:
                        shifts.append(f"[ODDS SHIFT] {home} home odds moved from {old_h:.2f} to {avg_home:.2f}")
                except:
                    pass

            new_data[sport_key][game_id] = {
                "game": f"{home} vs {away}",
                "time": datetime.fromisoformat(game['commence_time'].replace('Z', '+00:00')).strftime("%d %b, %H:%M"),
                "tip": current_tip,
                "odds": f"H:{avg_home:.2f} | A:{avg_away:.2f}"
            }

    save_history(new_data)
    
    # Output for Gemini LLM
    print("## CURRENT LIVE ODDS SUMMARY")
    print(json.dumps(new_data, indent=2))
    print("\n## DETECTED SHIFTS SINCE LAST RUN")
    if shifts:
        for s in shifts:
            print(f"- {s}")
    else:
        print("No significant shifts detected.")

if __name__ == "__main__":
    run_analysis()
