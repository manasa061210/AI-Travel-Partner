@echo off
echo =============================================
echo   AI Travel Partner - Building EXE for Windows
echo =============================================
echo.

cd backend

echo [1/3] Installing required packages...
pip install pyinstaller flask flask-sqlalchemy flask-cors pyjwt werkzeug python-dotenv requests

echo.
echo [2/3] Building EXE with PyInstaller...
pyinstaller --onefile --noconsole --name "AI-Travel-Partner" ^
  --add-data "static_react;static_react" ^
  --add-data "models;models" ^
  --add-data "routes;routes" ^
  --add-data "ai_modules;ai_modules" ^
  --hidden-import flask ^
  --hidden-import flask_sqlalchemy ^
  --hidden-import flask_cors ^
  --hidden-import jwt ^
  --hidden-import werkzeug ^
  --hidden-import sqlalchemy ^
  --hidden-import requests ^
  launcher.py

echo.
echo [3/3] Done!
echo.
echo Your EXE is ready at: backend\dist\AI-Travel-Partner.exe
echo.
echo IMPORTANT: Place your .env file next to the EXE before running.
echo .env file should contain:
echo   GROQ_API_KEY=your_key_here
echo   SECRET_KEY=travel-partner-secret-key-2026
echo   JWT_SECRET=travel-jwt-secret-2026
echo.
pause
