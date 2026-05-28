import time
from playwright.sync_api import sync_playwright

def record():
    print("[!] Connecting to your Footy Browser on port 9222...")
    with sync_playwright() as p:
        try:
            # Connect to your open browser
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            context = browser.contexts[0]
            page = context.pages[0] if context.pages else context.new_page()
            
            print("[!] OPENING THE RECORDER...")
            print("[!] A 'Playwright Inspector' window will appear.")
            print("[!] Go to your Footy Browser and perform your tipping.")
            print("[!] The code will be recorded in the Inspector window.")
            
            # This opens the recorder on your active page
            page.pause()
            
        except Exception as e:
            print(f"\n[ERROR] Could not connect: {e}")
            print("Make sure 'Footy Browser' is OPEN before running this.")

if __name__ == "__main__":
    record()
