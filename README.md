# Linear Programming Solver - One-Click Launcher

## Quick Start (One-Click Launch)

### For Windows Users:
1. **Double-click** `run_lp_solver.bat`
2. The application will automatically:
   - Check if Python is installed
   - Create a virtual environment (first time only)
   - Install required packages
   - Launch the Linear Programming Solver in your browser

### For Mac/Linux Users:
1. **Make the script executable** (first time only):
   ```bash
   chmod +x run_lp_solver.sh
   ```
2. **Double-click** `run_lp_solver.sh` or run in terminal:
   ```bash
   ./run_lp_solver.sh
   ```

## What the One-Click Launcher Does

✅ **Automatically checks** if Python is installed  
✅ **Creates virtual environment** (isolated Python environment)  
✅ **Installs all dependencies** (streamlit, numpy, pandas, matplotlib, pulp)  
✅ **Launches the application** in your default web browser  
✅ **Handles errors gracefully** with helpful messages  

## Manual Installation (Alternative)

If you prefer manual setup:

1. **Install Python 3.8+** from [python.org](https://www.python.org/downloads/)
2. **Open terminal/command prompt** in this folder
3. **Create virtual environment**:
   ```bash
   python -m venv lp_solver_env
   ```
4. **Activate virtual environment**:
   - Windows: `lp_solver_env\Scripts\activate`
   - Mac/Linux: `source lp_solver_env/bin/activate`
5. **Install dependencies**:
   ```bash
   pip install streamlit numpy pandas matplotlib pulp
   ```
6. **Run application**:
   ```bash
   streamlit run app.py
   ```

## Features

🔢 **Three Solution Methods**: Simplex, Graphical, Big M  
📊 **Step-by-step Solutions** with detailed explanations  
📈 **Visual Graphs** for 2-variable problems  
🎯 **Quick Start Templates** for common problem types  
✅ **Problem Validation** before solving  
📚 **Educational Content** and learning materials  
🔍 **Solution Analysis** with insights and interpretations  

## Troubleshooting

**"Python is not installed"**  
→ Download and install Python from [python.org](https://www.python.org/downloads/)

**"Failed to install packages"**  
→ Check your internet connection and try again

**Application doesn't open in browser**  
→ Manually go to `http://localhost:8501`

**Port already in use**  
→ Close other applications using port 8501 or restart your computer

## System Requirements

- **Python 3.8 or higher**
- **Internet connection** (for first-time package installation)
- **Web browser** (Chrome, Firefox, Safari, Edge)
- **2GB RAM minimum**

## Support

The application includes comprehensive help sections:
- **Example Problems** page with sample scenarios
- **About Methods** page explaining each algorithm
- **Solution Analysis** page with learning materials
- **Common Mistakes** guide for troubleshooting

---

**Ready to solve Linear Programming problems?** Just double-click the launcher for your operating system!