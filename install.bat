@echo off

:: Python installieren
echo Installing Python...
powershell -Command "Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.10.9/python-3.10.9-amd64.exe -OutFile python_installer.exe"
start /wait python_installer.exe /quiet InstallAllUsers=1 PrependPath=1

:: Warten, bis die Installation abgeschlossen ist
timeout /t 60

:: Pygame installieren
echo Installing Pygame...
py -m pip install pygame

:: Flappy.py ausführen
echo Running flappy.py...
py flappy.py

pause
