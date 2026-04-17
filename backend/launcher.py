import sys
import os
import threading
import webbrowser
import time

# PyInstaller bundles files into a temp folder (_MEIPASS)
# This makes sure all paths resolve correctly whether running as exe or script
if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
    EXE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    EXE_DIR = BASE_DIR

# Look for .env next to the exe
env_path = os.path.join(EXE_DIR, '.env')
if os.path.exists(env_path):
    from dotenv import load_dotenv
    load_dotenv(env_path)

# If GROQ_API_KEY not set, ask user on first run
if not os.environ.get('GROQ_API_KEY'):
    print("=" * 50)
    print("  AI Travel Partner - First Time Setup")
    print("=" * 50)
    print()
    print("You need a FREE Groq API key.")
    print("Get one at: https://console.groq.com")
    print()
    key = input("Paste your Groq API key: ").strip()
    os.environ['GROQ_API_KEY'] = key
    os.environ['SECRET_KEY'] = 'travel-partner-secret-key-2026'
    os.environ['JWT_SECRET'] = 'travel-jwt-secret-2026'

    with open(env_path, 'w') as f:
        f.write(f"GROQ_API_KEY={key}\n")
        f.write("SECRET_KEY=travel-partner-secret-key-2026\n")
        f.write("JWT_SECRET=travel-jwt-secret-2026\n")
    print("\nKey saved! Starting app...\n")

# Add base dir to path so Flask can find modules
sys.path.insert(0, BASE_DIR)

def open_browser():
    time.sleep(3)
    webbrowser.open('http://localhost:5000')

print("=" * 50)
print("  AI Travel Partner is starting...")
print("  Opening browser at: http://localhost:5000")
print("  Press Ctrl+C to stop the app")
print("=" * 50)

threading.Thread(target=open_browser, daemon=True).start()

from app import create_app
flask_app = create_app()
flask_app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
