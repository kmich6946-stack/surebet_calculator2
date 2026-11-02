@echo off
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
  echo Creating local Python environment...
  python -m venv .venv
  if errorlevel 1 (
    echo Failed to create the Python environment. Install Python 3 and try again.
    pause
    exit /b 1
  )
)

if not exist ".venv\flask-installed" (
  echo Installing calculator server dependency...
  ".venv\Scripts\python.exe" -m pip install -r requirements.txt
  if errorlevel 1 (
    echo Dependency installation failed.
    pause
    exit /b 1
  )
  type nul > ".venv\flask-installed"
)

".venv\Scripts\python.exe" start_local.py
if errorlevel 1 (
  echo Calculator could not be started.
  pause
)
