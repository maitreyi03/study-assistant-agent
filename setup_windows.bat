@echo off
setlocal

echo Creating a Python virtual environment...
python -m venv .venv
if errorlevel 1 goto error

echo Activating the virtual environment...
call .venv\Scripts\activate.bat
if errorlevel 1 goto error

echo Installing dependencies...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if errorlevel 1 goto error

if not exist .env (
    copy .env.example .env > nul
    echo.
    echo Created .env from .env.example.
    echo Open .env and add your Groq API key before running the agent.
)

echo.
echo Setup complete.
echo Activate the environment with: .venv\Scripts\activate
echo Run the agent with: python app.py
goto end

:error
echo.
echo Setup failed. Review the error message above.
exit /b 1

:end
endlocal
