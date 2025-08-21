# Linear Programming Solver

## Overview

This is a comprehensive educational Linear Programming (LP) solver built with Streamlit that provides step-by-step solutions using multiple mathematical methods. The application is designed to help students and professionals understand different LP solution techniques through interactive problem solving with detailed explanations and visualizations.

The solver supports various LP problem types (maximization/minimization) and implements three core solution methods: Simplex Method, Graphical Method (for 2-variable problems), and Big M Method for handling artificial variables. The application includes sample problems, mathematical formatting, educational content, solution analysis tools, and interactive templates to enhance learning.

## Recent Updates (August 2025)

### Enhanced User Interface
- Added informational cards showing method capabilities on the main page
- Implemented quick start templates for common problem types
- Enhanced sidebar navigation with user guidance
- Added problem validation system with detailed error messages

### New Solution Analysis Page
- Method comparison table showing when to use each approach
- Sensitivity analysis explanations with shadow prices
- Common LP problem types with detailed descriptions
- Common mistakes section with solutions and best practices

### Improved Problem Input
- Template-based quick start for Production Planning, Resource Allocation, Diet Problems, and Investment Portfolio
- Real-time problem validation before solving
- Enhanced constraint input with default values from templates
- Method-specific recommendations and warnings

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit web application with multi-page navigation
- **UI Components**: Sidebar navigation, column layouts, interactive forms, and mathematical displays
- **Visualization**: Matplotlib integration for graphical method plotting with feasible region visualization
- **Page Structure**: Three main sections - Problem Input, Example Problems, and About Methods

### Backend Architecture
- **Modular Solver Design**: Separate solver classes for each mathematical method (SimplexSolver, GraphicalSolver, BigMSolver)
- **Step-by-Step Processing**: Each solver maintains iteration history and detailed solution steps
- **Mathematical Processing**: NumPy for numerical computations and tableau operations
- **Problem Representation**: Dictionary-based data structures for LP problem formulation

### Core Components
- **Input Processing**: InputParser class handles user input validation and conversion to standard LP format
- **Problem Formatting**: ProblemFormatter converts internal representations to mathematical notation
- **Solution Methods**:
  - Simplex Method: Standard tableau-based implementation with pivot operations
  - Graphical Method: Constraint plotting and corner point evaluation for 2-variable problems
  - Big M Method: Artificial variable technique for equality constraints
- **Educational Content**: Sample problems with descriptions, formulations, and solutions

### Data Flow Architecture
- **Input Validation**: Parse and validate objective functions, constraints, and problem parameters
- **Problem Conversion**: Transform user input into standardized mathematical format
- **Solution Processing**: Apply selected mathematical method with step tracking
- **Result Presentation**: Format solutions with detailed explanations and visualizations

## External Dependencies

### Core Libraries
- **Streamlit**: Web application framework for interactive UI
- **NumPy**: Numerical computing for matrix operations and mathematical calculations
- **Pandas**: Data manipulation for tableau representation and display
- **Matplotlib**: Plotting library for graphical method visualizations
- **PuLP**: Linear programming library (imported but usage not evident in provided code)

### Mathematical Components
- **NumPy Arrays**: Matrix operations for simplex tableau manipulations
- **Matplotlib Backends**: Non-GUI backend configuration for server deployment
- **Pandas DataFrames**: Structured display of solution tableaux and iterations

### Utility Dependencies
- **Python Standard Library**: Regular expressions (re) for input parsing and typing for type hints
- **Mathematical Notation**: Unicode subscripts and mathematical symbols for proper formatting