import os
import json
import logging
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
        print(f"Failed to fetch {sport_key}: {e}")
        return []

def get_game_data():
    all_games = []
    for sport_key, sport_name in SPORTS.items():
        raw_data = fetch_odds(sport_key)
        for game in raw_data:
            home_team = game['home_team']
            away_team = game['away_team']
            commence_time = game['commence_time']
            
            odds_pool = {home_team: [], away_team: []}
            for bookmaker in game.get('bookmakers', []):
                if bookmaker['key'] in BOOKMAKERS_TO_CHECK:
                    for market in bookmaker.get('markets', []):
                        if market['key'] == 'h2h':
                            for outcome in market['outcomes']:
                                odds_pool[outcome['name']].append(outcome['price'])
            
            avg_home = sum(odds_pool[home_team]) / len(odds_pool[home_team]) if odds_pool[home_team] else 0
            avg_away = sum(odds_pool[away_team]) / len(odds_pool[away_team]) if odds_pool[away_team] else 0
            
            all_games.append({
                "sport": sport_name,
                "home": home_team,
                "away": away_team,
                "time": commence_time,
                "odds_home": round(avg_home, 2),
                "odds_away": round(avg_away, 2)
            })
    return all_games

def generate_llm_prompt(games, news_context=""):
    prompt = f"""
# FOOTY TIPPING ANALYSIS PROMPT
Date: {datetime.now().strftime('%Y-%m-%d')}

You are an expert Footy Tipping Analyst for AFL and NRL. 
Your goal is to provide the best possible tips for this week's games.

## Weighting Criteria:
1. **Betting Odds (Primary):** The favorite is usually the safest bet.
2. **Key Players (Secondary):** If key players are out, it can swing a game, especially if odds are close.
3. **Ladder Position (Tertiary):** Current standing in the season. (Note: Early season means ladder is less relevant).

## Games & Odds:
{json.dumps(games, indent=2)}

## Latest News Context:
{news_context}

## Instructions:
For each game:
1. Analyze the odds.
2. Consider the news/injuries.
3. Provide a "Recommended Tip".
4. Provide a "Confidence Level" (High, Medium, Low).
5. Give a 1-sentence "Reasoning".

Format the output as a clean Markdown table.
"""
    return prompt

if __name__ == "__main__":
    print("Fetching latest odds...")
    games = get_game_data()
    
    # In a real scenario, we might call another tool here to get news_context
    # For now, I'll just print the prompt template
    prompt = generate_llm_prompt(games, "ADD LATEST INJURY NEWS HERE")
    
    with open('llm_prompt.md', 'w') as f:
        f.write(prompt)
    
    print("LLM Prompt generated in 'llm_prompt.md'.")
