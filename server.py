from flask import Flask
import subprocess
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

# The path to your tipping script
SCRIPT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src", "main.py")

@app.route('/run-tips', methods=['GET'])
def run_tips():
    logging.info("Phone trigger received! Starting Footy Bot...")
    try:
        # Run the tipping script in the background
        subprocess.Popen(['python3', SCRIPT_PATH])
        return "Bot Started! Check your laptop for the report.", 200
    except Exception as e:
        logging.error(f"Failed to start bot: {e}")
        return f"Error: {e}", 500

if __name__ == '__main__':
    print("\n" + "="*40)
    print("FOOTY BOT SERVER IS RUNNING")
    print("Listening for phone trigger...")
    print("="*40 + "\n")
    # Listen on all network interfaces on port 5000
    app.run(host='0.0.0.0', port=5000)
