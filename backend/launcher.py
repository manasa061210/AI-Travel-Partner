import threading
import webbrowser
import time
import sys
import os

# Load .env if it exists next to the exe
env_path = os.path.join(os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else __file__), '.env')
if os.path.exists(env_path):
    from dotenv import load_dotenv
    load_dotenv(env_path)

# If GROQ_API_KEY not set, ask user
if not os.environ.get('GROQ_API_KEY'):
    print("=" * 50)
    print("  AI Travel Partner — First Time Setup")
    print("=" * 50)
    print("\nYou need a FREE Groq API key to use this app.")
    print("Get one at: https://console.groq.com")
    print()
    key = input("Paste your Groq API key here: ").strip()
    os.environ['GROQ_API_KEY'] = key

    # Save to .env for next time
    with open(env_path, 'w') as f:
        f.write(f"GROQ_API_KEY={key}\n")
        f.write("SECRET_KEY=travel-partner-secret-key-2026\n")
        f.write("JWT_SECRET=travel-jwt-secret-2026\n")
    print("\nKey saved. Starting app...\n")

def open_browser():
    time.sleep(2)
    webbrowser.open('http://localhost:5000')

def run():
    print("=" * 50)
    print("  AI Travel Partner is starting...")
    print("  Open: http://localhost:5000")
    print("  Press Ctrl+C to stop")
    print("=" * 50)

    threading.Thread(target=open_browser, daemon=True).start()

    from app import create_app
    flask_app = create_app()
    flask_app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

if __name__ == '__main__':
    run()
