import logging
import time
import re
from playwright.sync_api import sync_playwright

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def safe_click(locator, name="element"):
    """Helper to click an element while handling 'detached' and 'ValueError' crashes."""
    for i in range(3):
        try:
            if locator.is_visible(timeout=3000):
                locator.scroll_into_view_if_needed()
                locator.click(force=True)
                return True
        except Exception as e:
            logging.info(f"Retrying click on {name}... (attempt {i+1})")
            time.sleep(1.5)
    return False

def run_tipping(nrl_tips, afl_tips, headless=False):
    with sync_playwright() as p:
        try:
            if headless:
                logging.info("Starting HEADLESS browser with persistent profile...")
                # Launch persistent context instead of connecting to CDP
                user_data_dir = "/home/ross/FootyTip/bot_profile"
                context = p.chromium.launch_persistent_context(
                    user_data_dir,
                    headless=True,
                    args=["--remote-debugging-port=9222"] # Keep port open just in case
                )
                page = context.new_page()
            else:
                logging.info("Connecting to 'Footy Browser' via CDP...")
                # Connect to your open browser
                try:
                    browser = p.chromium.connect_over_cdp("http://localhost:9222")
                    context = browser.contexts[0]
                    
                    # 1. Find the FootyTips tab
                    page = None
                    for p_obj in context.pages:
                        if "footytips" in p_obj.url.lower():
                            page = p_obj
                            break
                    
                    if not page:
                        logging.error("FootyTips tab not found! Opening a new one...")
                        page = context.new_page()
                except Exception as e:
                    logging.error(f"Could not connect to browser: {e}")
                    logging.info("Make sure 'Footy Browser' is OPEN if not running in --headless mode.")
                    return

            page.bring_to_front()


            # 2. Process each sport
            for sport_name, tips in [("NRL", nrl_tips), ("AFL", afl_tips)]:
                if not tips: continue
                
                logging.info(f"--- {sport_name} ---")
                target_url = f"footytips.com.au/tipping/{sport_name.lower()}"
                
                # Only navigate if we aren't already there
                if target_url not in page.url.lower():
                    logging.info(f"Navigating to {target_url}...")
                    try:
                        page.goto(f"https://www.{target_url}", wait_until="domcontentloaded", timeout=20000)
                    except:
                        pass
                
                # Wait for the page to be TRULY stable
                time.sleep(5)
                try:
                    page.wait_for_load_state("networkidle", timeout=10000)
                except:
                    pass

                # 3. Place tips
                logging.info(f"Placing {len(tips)} tips...")
                for game_id, data in tips.items():
                    team = data['tip']
                    team_short = team.split()[-1]
                    
                    # Try to find the radio button
                    clicked = False
                    for t_name in [team, team_short]:
                        try:
                            row = page.locator(f".MuiFormControlLabel-root:has-text('{t_name}')").first
                            radio = row.locator(".MuiButtonBase-root").first
                            if safe_click(radio, team):
                                logging.info(f"  [OK] {team}")
                                clicked = True
                                break
                        except:
                            continue
                    
                    if not clicked:
                        logging.warning(f"  [!] Could not click {team}")
                    time.sleep(0.3)

                # 4. Submit
                logging.info("Finalizing: Clicking 'SubmitTips'...")
                try:
                    submit_btn = page.get_by_role("button", name="SubmitTips").first
                    if not safe_click(submit_btn, "SubmitTips"):
                        # Fallback for dynamic names
                        fallback = page.get_by_role("button", name=re.compile("Submit", re.IGNORECASE)).first
                        safe_click(fallback, "Fallback Submit")
                except Exception as e:
                    logging.error(f"Submit failed: {e}")

        except Exception as e:
            logging.error(f"Fatal error: {e}")
        finally:
            logging.info("Bot process finished.")

if __name__ == "__main__":
    pass
