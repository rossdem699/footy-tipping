import os
import time
import logging
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_driver():
    logging.info("Attempting to connect to your Chrome Browser...")
    chrome_options = Options()
    # This tells the bot to 'hijack' the Chrome window we're about to open
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        return driver
    except Exception as e:
        logging.error(f"Could not connect to Chrome! Error: {e}")
        return None

def submit_tips_to_competition(driver, competition_name, tips):
    logging.info(f"Looking for tips for: {competition_name}...")
    
    # Check if we are already on the tipping page or need to go to the dashboard
    if competition_name.lower() not in driver.title.lower():
        logging.info(f"Navigating to Dashboard to find: {competition_name}...")
        driver.get("https://www.footytips.com.au/tipping")
        time.sleep(8)
        
        # Find and click the competition link
        comp_xpath = f"//a[contains(translate(text(), 'MACNR', 'macnr'), 'macca') and contains(translate(text(), 'NRLAF', 'nrlaf'), '{competition_name[-3:].lower()}')]"
        comp_links = driver.find_elements(By.XPATH, comp_xpath)
        
        if comp_links:
            comp_links[0].click()
            time.sleep(8)
        else:
            logging.error(f"Could not find competition: {competition_name} on the dashboard.")
            return

    logging.info(f"Processing tips for {competition_name}...")
    
    # Place tips
    for game_id, tip_data in tips.items():
        tip_team = tip_data['tip']
        logging.info(f"  > Tipping: {tip_team}")
        
        try:
            # Flexible button search
            btn_xpath = f"//button[contains(text(), '{tip_team}')] | //div[contains(text(), '{tip_team}')]/ancestor::button"
            btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, btn_xpath)))
            driver.execute_script("arguments[0].scrollIntoView(true);", btn)
            time.sleep(1)
            btn.click()
            logging.info(f"    [OK] Clicked '{tip_team}'")
        except Exception:
            logging.warning(f"    [!] Could not click '{tip_team}'. Skipping...")
    
    # Final Submit
    try:
        submit_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Submit') or contains(text(), 'Save')]")
        submit_btn.click()
        logging.info(f"SUCCESS: Tips submitted for {competition_name}!")
        time.sleep(3)
    except Exception:
        logging.warning("Could not find the 'Submit' button. Please click it manually!")


def main(nrl_tips, afl_tips):
    driver = get_driver()
    if not driver:
        print("\n[!] Chrome is not in 'Remote Mode'. Fixing this now...")
        return False

    try:
        # Place NRL
        if nrl_tips:
            submit_tips_to_competition(driver, "macca nrl footy tippers", nrl_tips)
        
        # Place AFL
        if afl_tips:
            submit_tips_to_competition(driver, "macca afl footy tippers", afl_tips)
            
        return True
    except Exception as e:
        logging.error(f"Automation failed: {e}")
        return False
