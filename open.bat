@echo off

:: Überprüfen, ob Python installiert ist
echo Checking Python installation...
py --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not added to PATH.
    echo Please install Python and ensure it is added to the system PATH.
    pause
    exit /b
)

:: Flappy.py ausführen
echo Starting flappy.py...
py flappy.py

exit
