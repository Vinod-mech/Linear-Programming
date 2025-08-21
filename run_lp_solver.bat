@echo off
echo Starting Linear Programming Solver...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "lp_solver_env" (
    echo Creating virtual environment...
    python -m venv lp_solver_env
    if errorlevel 1 (
        echo Error: Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo Activating virtual environment...
call lp_solver_env\Scripts\activate.bat

REM Install/upgrade required packages
echo Installing required packages...
pip install --quiet --upgrade streamlit numpy pandas matplotlib pulp

REM Check if installation was successful
if errorlevel 1 (
    echo Error: Failed to install required packages
    echo Please check your internet connection and try again
    pause
    exit /b 1
)

REM Start the application
echo.
echo Starting Linear Programming Solver...
echo The application will open in your default web browser.
echo To stop the application, close this window or press Ctrl+C
echo.

streamlit run app.py --server.port 8501

REM If we get here, streamlit has stopped
echo.
echo Linear Programming Solver has stopped.
pause