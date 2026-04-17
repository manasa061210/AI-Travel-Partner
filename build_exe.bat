@echo off
echo =============================================
echo   AI Travel Partner - Building EXE for Windows
echo =============================================
echo.

cd backend

echo [1/3] Installing required packages...
pip install pyinstaller flask flask-sqlalchemy flask-cors pyjwt werkzeug python-dotenv requests groq
if %errorlevel% neq 0 (
    echo ERROR: pip install failed. Make sure Python is installed.
    pause
    exit /b 1
)

echo.
echo [2/3] Cleaning previous build...
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
if exist AI-Travel-Partner.spec del AI-Travel-Partner.spec

echo.
echo [3/3] Building EXE with PyInstaller...
pyinstaller --onefile ^
  --console ^
  --name "AI-Travel-Partner" ^
  --add-data "static_react;static_react" ^
  --add-data "models;models" ^
  --add-data "routes;routes" ^
  --add-data "ai_modules;ai_modules" ^
  --hidden-import=flask ^
  --hidden-import=flask_sqlalchemy ^
  --hidden-import=flask_cors ^
  --hidden-import=flask.templating ^
  --hidden-import=flask_cors.extension ^
  --hidden-import=jwt ^
  --hidden-import=jwt.algorithms ^
  --hidden-import=werkzeug ^
  --hidden-import=werkzeug.security ^
  --hidden-import=sqlalchemy ^
  --hidden-import=sqlalchemy.dialects.sqlite ^
  --hidden-import=sqlalchemy.orm ^
  --hidden-import=requests ^
  --hidden-import=dotenv ^
  --hidden-import=groq ^
  --hidden-import=email.mime.text ^
  --hidden-import=email.mime.multipart ^
  --collect-all flask ^
  --collect-all flask_sqlalchemy ^
  --collect-all flask_cors ^
  launcher.py

if %errorlevel% neq 0 (
    echo.
    echo ERROR: PyInstaller failed. See errors above.
    pause
    exit /b 1
)

echo.
echo =============================================
echo  SUCCESS! EXE created at: backend\dist\AI-Travel-Partner.exe
echo =============================================
echo.
echo Before running the EXE, create a .env file
echo in the same folder as the EXE with this content:
echo.
echo   GROQ_API_KEY=your_groq_api_key_here
echo   SECRET_KEY=travel-partner-secret-key-2026
echo   JWT_SECRET=travel-jwt-secret-2026
echo.
pause
