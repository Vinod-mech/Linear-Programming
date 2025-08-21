#!/bin/bash

echo "Starting Linear Programming Solver..."
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "Error: Python is not installed"
        echo "Please install Python from https://www.python.org/downloads/"
        read -p "Press Enter to exit..."
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

echo "Using Python: $PYTHON_CMD"

# Check if virtual environment exists
if [ ! -d "lp_solver_env" ]; then
    echo "Creating virtual environment..."
    $PYTHON_CMD -m venv lp_solver_env
    if [ $? -ne 0 ]; then
        echo "Error: Failed to create virtual environment"
        read -p "Press Enter to exit..."
        exit 1
    fi
fi

# Activate virtual environment
echo "Activating virtual environment..."
source lp_solver_env/bin/activate

# Install/upgrade required packages
echo "Installing required packages..."
pip install --quiet --upgrade streamlit numpy pandas matplotlib pulp

if [ $? -ne 0 ]; then
    echo "Error: Failed to install required packages"
    echo "Please check your internet connection and try again"
    read -p "Press Enter to exit..."
    exit 1
fi

# Start the application
echo
echo "Starting Linear Programming Solver..."
echo "The application will open in your default web browser."
echo "To stop the application, press Ctrl+C in this terminal"
echo

streamlit run app.py --server.port 8501

# If we get here, streamlit has stopped
echo
echo "Linear Programming Solver has stopped."
read -p "Press Enter to exit..."