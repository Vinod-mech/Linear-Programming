import streamlit as st
import numpy as np
import pulp
from solvers.simplex_method import SimplexSolver
from solvers.graphical_method import GraphicalSolver
from solvers.big_m_method import BigMSolver
from utils.input_parser import InputParser
from utils.problem_formatter import ProblemFormatter
from examples.sample_problems import get_sample_problems

def main():
    st.set_page_config(
        page_title="Linear Programming Solver",
        page_icon="📊",
        layout="wide"
    )
    
    st.title("📊 Linear Programming Solver")
    st.markdown("**Educational Operational Research Tool** - Solve Linear Programming problems with detailed step-by-step solutions using multiple methods")
    
    # Add quick info cards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("🔢 **Simplex Method**\nStandard algorithm for LP problems")
    with col2:
        st.info("📈 **Graphical Method**\nVisual solution for 2-variable problems") 
    with col3:
        st.info("🎯 **Big M Method**\nHandles equality & ≥ constraints")
    
    # Sidebar for navigation
    with st.sidebar:
        st.header("🧭 Navigation")
        page = st.radio(
            "Select Page",
            ["Problem Input", "Example Problems", "About Methods", "Solution Analysis"]
        )
        
        st.markdown("---")
        st.markdown("**📚 Quick Guide:**")
        st.markdown("• Start with **Example Problems** to learn")
        st.markdown("• Use **Problem Input** for custom problems")
        st.markdown("• Check **About Methods** for theory")
        st.markdown("• View **Solution Analysis** for insights")
    
    if page == "Problem Input":
        show_problem_input()
    elif page == "Example Problems":
        show_example_problems()
    elif page == "About Methods":
        show_about_methods()
    else:
        show_solution_analysis()

def show_problem_input():
    st.header("🔧 Linear Programming Problem Input")
    
    # Add template selection
    st.subheader("Quick Start")
    template = st.selectbox(
        "Choose a template to get started faster:",
        ["Start from scratch", "Production Planning", "Resource Allocation", "Diet Problem", "Investment Portfolio"]
    )
    
    if template != "Start from scratch":
        st.info(f"✨ Template '{template}' loaded! You can modify the values below.")
        # Load template data
        templates = {
            "Production Planning": {"obj": "3, 2", "constraints": [("2, 1", "≤", 100), ("1, 2", "≤", 80)]},
            "Resource Allocation": {"obj": "25, 40", "constraints": [("4, 3", "≤", 240), ("2, 6", "≤", 300)]},
            "Diet Problem": {"obj": "2, 3", "constraints": [("1, 2", "≥", 8), ("3, 1", "≥", 12)]},
            "Investment Portfolio": {"obj": "0.08, 0.12", "constraints": [("1, 1", "≤", 10000), ("1, 0", "≥", 3000), ("0, 1", "≤", 6000)]}
        }
    
    # Problem type selection
    col1, col2 = st.columns(2)
    with col1:
        problem_type = st.selectbox(
            "Problem Type",
            ["Maximize", "Minimize"]
        )
    
    with col2:
        method = st.selectbox(
            "Solution Method",
            ["Simplex Method", "Graphical Method", "Big M Method"]
        )
    
    # Add method recommendation
    if method == "Graphical Method":
        st.warning("⚠️ Graphical Method works only for 2-variable problems")
    elif method == "Big M Method":
        st.info("💡 Big M Method is best for problems with equality constraints or ≥ constraints")
    
    # Objective function input
    st.subheader("Objective Function")
    st.markdown("Enter coefficients for the objective function (e.g., for 3x₁ + 2x₂, enter '3, 2')")
    
    # Use template data if available
    default_obj = ""
    if template != "Start from scratch":
        default_obj = templates[template]["obj"]
    
    obj_coeffs = st.text_input(
        "Objective Function Coefficients",
        value=default_obj,
        placeholder="3, 2, 1",
        help="Enter coefficients separated by commas"
    )
    
    # Number of constraints
    num_constraints = st.number_input(
        "Number of Constraints",
        min_value=1,
        max_value=10,
        value=2
    )
    
    # Constraints input
    st.subheader("Constraints")
    constraints = []
    
    # Load template constraints if applicable
    template_constraints = []
    if template != "Start from scratch":
        template_constraints = templates[template]["constraints"]
    
    for i in range(num_constraints):
        st.markdown(f"**Constraint {i+1}:**")
        col1, col2, col3 = st.columns([3, 1, 1])
        
        # Set defaults from template
        default_coeffs = ""
        default_type = "≤"
        default_rhs = 0.0
        
        if i < len(template_constraints):
            default_coeffs = template_constraints[i][0]
            default_type = template_constraints[i][1]
            default_rhs = template_constraints[i][2]
        
        with col1:
            constraint_coeffs = st.text_input(
                f"Coefficients for constraint {i+1}",
                key=f"constraint_{i}_coeffs",
                value=default_coeffs,
                placeholder="2, 1",
                help="Enter coefficients separated by commas"
            )
        
        with col2:
            type_options = ["≤", "≥", "="]
            default_index = type_options.index(default_type) if default_type in type_options else 0
            constraint_type = st.selectbox(
                "Type",
                type_options,
                key=f"constraint_{i}_type",
                index=default_index
            )
        
        with col3:
            rhs = st.number_input(
                "RHS",
                key=f"constraint_{i}_rhs",
                value=default_rhs
            )
        
        if constraint_coeffs:
            constraints.append({
                'coefficients': constraint_coeffs,
                'type': constraint_type,
                'rhs': rhs
            })
    
    # Non-negativity constraints
    st.subheader("Variable Constraints")
    non_negativity = st.checkbox(
        "All variables are non-negative (xᵢ ≥ 0)",
        value=True
    )
    
    # Problem validation and solve
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔍 Validate Problem", help="Check if the problem is properly formulated"):
            if obj_coeffs and len(constraints) > 0:
                validation_result = validate_problem_input(obj_coeffs, constraints)
                if validation_result['valid']:
                    st.success("✅ Problem is well-formulated!")
                    st.markdown("**Problem Summary:**")
                    st.markdown(f"• Variables: {validation_result['num_variables']}")
                    st.markdown(f"• Constraints: {len(constraints)}")
                    st.markdown(f"• Problem type: {problem_type}")
                else:
                    st.error(f"❌ Problem validation failed: {validation_result['error']}")
            else:
                st.error("Please enter the objective function and at least one constraint.")
    
    with col2:
        if st.button("🚀 Solve Problem", type="primary"):
            if obj_coeffs and len(constraints) > 0:
                validation_result = validate_problem_input(obj_coeffs, constraints)
                if validation_result['valid']:
                    solve_problem(problem_type, method, obj_coeffs, constraints, non_negativity)
                else:
                    st.error(f"Cannot solve: {validation_result['error']}")
            else:
                st.error("Please enter the objective function and at least one constraint.")

def validate_problem_input(obj_coeffs, constraints):
    """Validate problem input before solving"""
    try:
        # Parse objective coefficients
        obj_list = [float(x.strip()) for x in obj_coeffs.split(',') if x.strip()]
        if not obj_list:
            return {'valid': False, 'error': 'Empty objective function'}
        
        num_vars = len(obj_list)
        
        # Check constraints
        for i, constraint in enumerate(constraints):
            if not constraint['coefficients'].strip():
                return {'valid': False, 'error': f'Empty coefficients in constraint {i+1}'}
            
            constraint_coeffs = [float(x.strip()) for x in constraint['coefficients'].split(',') if x.strip()]
            
            if len(constraint_coeffs) != num_vars:
                return {'valid': False, 'error': f'Constraint {i+1} has {len(constraint_coeffs)} variables, expected {num_vars}'}
            
            if constraint['rhs'] is None:
                return {'valid': False, 'error': f'Missing RHS value in constraint {i+1}'}
        
        return {'valid': True, 'num_variables': num_vars}
        
    except ValueError as e:
        return {'valid': False, 'error': f'Invalid number format: {str(e)}'}
    except Exception as e:
        return {'valid': False, 'error': f'Validation error: {str(e)}'}

def solve_problem(problem_type, method, obj_coeffs, constraints, non_negativity):
    try:
        # Parse input
        parser = InputParser()
        parsed_problem = parser.parse_problem(
            problem_type, obj_coeffs, constraints, non_negativity
        )
        
        if parsed_problem['error']:
            st.error(parsed_problem['error'])
            return
        
        # Display formatted problem
        formatter = ProblemFormatter()
        st.subheader("Problem Formulation")
        st.markdown(formatter.format_problem(parsed_problem))
        
        # Solve using selected method
        st.subheader(f"Solution using {method}")
        
        if method == "Simplex Method":
            solver = SimplexSolver()
            result = solver.solve(parsed_problem)
        elif method == "Graphical Method":
            if len(parsed_problem['objective']) > 2:
                st.error("Graphical method only supports problems with 2 variables.")
                return
            solver = GraphicalSolver()
            result = solver.solve(parsed_problem)
        else:  # Big M Method
            solver = BigMSolver()
            result = solver.solve(parsed_problem)
        
        # Display results
        display_solution(result, method)
        
    except Exception as e:
        st.error(f"An error occurred while solving the problem: {str(e)}")

def display_solution(result, method):
    if result['status'] == 'error':
        st.error(result['message'])
        return
    
    # Show step-by-step solution
    if 'steps' in result:
        st.subheader("Step-by-Step Solution")
        for i, step in enumerate(result['steps'], 1):
            with st.expander(f"Step {i}: {step['title']}", expanded=i==1):
                st.markdown(step['explanation'])
                if 'table' in step:
                    st.dataframe(step['table'])
                if 'figure' in step:
                    st.pyplot(step['figure'])
    
    # Show final solution
    st.subheader("Final Solution")
    
    if result['status'] == 'optimal':
        st.success("✅ Optimal solution found!")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**Decision Variables:**")
            for var, value in result['variables'].items():
                st.write(f"{var} = {value:.4f}")
        
        with col2:
            st.markdown("**Objective Value:**")
            st.write(f"Z = {result['objective_value']:.4f}")
        
        with col3:
            st.markdown("**Solution Type:**")
            st.write("Basic Feasible Solution")
            st.write("Corner Point of Feasible Region")
        
        # Add solution interpretation
        st.subheader("💡 Solution Interpretation")
        total_variables = len(result['variables'])
        basic_variables = sum(1 for value in result['variables'].values() if value > 0.001)
        
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"**Active Variables:** {basic_variables} out of {total_variables}")
            st.markdown("Variables with positive values in the optimal solution")
        
        with col2:
            st.info(f"**Method Used:** {method}")
            if method == "Graphical Method":
                st.markdown("Solution found by evaluating corner points")
            elif method == "Simplex Method":
                st.markdown("Solution found through tableau iterations")
            else:
                st.markdown("Solution found using artificial variables")
    
    elif result['status'] == 'unbounded':
        st.warning("⚠️ The problem is unbounded.")
        st.markdown("**Meaning:** The objective function can be increased indefinitely.")
        st.markdown("**Cause:** The feasible region extends infinitely in the direction of optimization.")
        st.markdown("**Action:** Check if constraints are missing or incorrectly formulated.")
    
    elif result['status'] == 'infeasible':
        st.error("❌ The problem is infeasible.")
        st.markdown("**Meaning:** There is no solution that satisfies all constraints simultaneously.")
        st.markdown("**Cause:** Constraints are contradictory or too restrictive.")
        st.markdown("**Action:** Review constraints for conflicts or relax some requirements.")
    
    else:
        st.info(f"Status: {result['status']}")
        
    # Add learning insights
    if result['status'] == 'optimal':
        st.subheader("🎓 Learning Insights")
        insights = []
        
        # Check for tight constraints (this would need constraint analysis)
        insights.append("💡 In optimal solutions, at least n constraints are tight (where n = number of variables)")
        
        if method == "Graphical Method":
            insights.append("📈 Graphical method shows that optimal solutions occur at corner points")
        
        if method == "Simplex Method":
            insights.append("🔢 Simplex method efficiently moves from one corner point to a better one")
        
        if method == "Big M Method":
            insights.append("🎯 Big M method handles complex constraint types by using artificial variables")
        
        for insight in insights:
            st.markdown(insight)

def show_example_problems():
    st.header("Example Problems")
    st.markdown("Select from pre-defined problems to understand the solving process:")
    
    examples = get_sample_problems()
    
    selected_example = st.selectbox(
        "Choose an example",
        list(examples.keys())
    )
    
    if selected_example:
        problem = examples[selected_example]
        
        st.subheader(f"Example: {selected_example}")
        st.markdown(problem['description'])
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Problem Formulation:**")
            st.code(problem['formulation'], language='text')
        
        with col2:
            st.markdown("**Expected Solution:**")
            st.code(problem['solution'], language='text')
        
        if st.button("Load This Example"):
            # Store example data in session state for use in Problem Input
            st.session_state.example_data = problem['data']
            st.success("Example loaded! Go to 'Problem Input' to solve.")

def show_about_methods():
    st.header("Solution Methods")
    
    methods = {
        "Simplex Method": {
            "description": """
            The Simplex Method is the most widely used algorithm for solving linear programming problems.
            It systematically examines the vertices of the feasible region to find the optimal solution.
            
            **Key Features:**
            - Works for problems with any number of variables
            - Provides complete step-by-step tableaux
            - Shows basis changes and pivot operations
            - Handles both maximization and minimization problems
            
            **When to Use:**
            - Standard form linear programming problems
            - Problems with more than 2 variables
            - When you need detailed algebraic steps
            """,
            "steps": [
                "Convert problem to standard form",
                "Set up initial simplex tableau",
                "Identify entering and leaving variables",
                "Perform pivot operations",
                "Check for optimality",
                "Repeat until optimal solution is found"
            ]
        },
        
        "Graphical Method": {
            "description": """
            The Graphical Method solves linear programming problems by plotting constraints
            and finding the optimal point on the feasible region boundary.
            
            **Key Features:**
            - Visual representation of the problem
            - Easy to understand and interpret
            - Shows feasible region clearly
            - Limited to 2-variable problems
            
            **When to Use:**
            - Problems with exactly 2 decision variables
            - Educational purposes to visualize LP concepts
            - Quick solutions for simple problems
            """,
            "steps": [
                "Plot constraint lines on coordinate system",
                "Identify feasible region",
                "Find corner points of feasible region",
                "Evaluate objective function at each corner point",
                "Select the optimal corner point"
            ]
        },
        
        "Big M Method": {
            "description": """
            The Big M Method is used to solve linear programming problems that are not
            in standard form, particularly those with equality constraints or ≥ constraints.
            
            **Key Features:**
            - Handles mixed constraint types (≤, ≥, =)
            - Uses artificial variables with large penalty coefficients
            - Converts any LP problem to standard form
            - Detects infeasible solutions
            
            **When to Use:**
            - Problems with equality constraints
            - Problems with ≥ constraints
            - Mixed constraint problems
            - When other methods are not directly applicable
            """,
            "steps": [
                "Add slack, surplus, and artificial variables",
                "Assign big M coefficients to artificial variables",
                "Set up modified simplex tableau",
                "Solve using simplex method",
                "Check if artificial variables are in final solution",
                "Interpret results based on artificial variable values"
            ]
        }
    }
    
    for method_name, method_info in methods.items():
        with st.expander(f"{method_name}", expanded=False):
            st.markdown(method_info['description'])
            
            st.markdown("**Solution Steps:**")
            for i, step in enumerate(method_info['steps'], 1):
                st.markdown(f"{i}. {step}")

def show_solution_analysis():
    st.header("📊 Solution Analysis & Learning")
    
    st.markdown("""
    This section helps you understand Linear Programming concepts and analyze solution patterns.
    """)
    
    # Tabs for different analysis types
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Method Comparison", "🎯 Sensitivity Analysis", "📝 Problem Types", "🔍 Common Mistakes"])
    
    with tab1:
        st.subheader("When to Use Each Method")
        
        method_comparison = {
            "Problem Type": ["2 variables, ≤ constraints", "Any variables, standard form", "Mixed constraints (=, ≥)", "Large problems"],
            "Graphical Method": ["✅ Best choice", "❌ Not applicable", "❌ Complex setup", "❌ Not practical"],
            "Simplex Method": ["✅ Works well", "✅ Optimal choice", "⚠️ Needs conversion", "✅ Efficient"],
            "Big M Method": ["✅ Works", "✅ Works", "✅ Best choice", "⚠️ Computational cost"]
        }
        
        import pandas as pd
        df = pd.DataFrame(method_comparison)
        st.dataframe(df, use_container_width=True)
        
        st.markdown("**💡 Quick Tips:**")
        st.markdown("• Start with Graphical Method for 2-variable problems to visualize")
        st.markdown("• Use Simplex Method for standard form problems")
        st.markdown("• Choose Big M Method when you have equality constraints")
    
    with tab2:
        st.subheader("Understanding Solution Sensitivity")
        
        st.markdown("""
        **What happens when parameters change?**
        
        1. **Objective Function Coefficients**: Changes affect which corner point is optimal
        2. **Right-Hand Side (RHS)**: Changes affect feasible region size
        3. **Constraint Coefficients**: Changes affect constraint line slopes
        """)
        
        st.info("💡 Try modifying the RHS values in example problems to see how solutions change!")
        
        # Shadow prices explanation
        st.markdown("**Shadow Prices (Dual Values):**")
        st.markdown("• Show how much the objective function increases per unit increase in RHS")
        st.markdown("• Help identify which constraints are most valuable to relax")
        st.markdown("• Only valid within a certain range (sensitivity range)")
    
    with tab3:
        st.subheader("Common Linear Programming Problem Types")
        
        problem_types = {
            "Production Planning": {
                "Description": "Determine optimal production quantities",
                "Variables": "Units of products to produce",
                "Objective": "Maximize profit or minimize cost",
                "Constraints": "Resource limits (labor, materials, capacity)"
            },
            "Diet Problem": {
                "Description": "Find minimum cost diet meeting nutrition requirements",
                "Variables": "Quantities of different foods",
                "Objective": "Minimize total cost",
                "Constraints": "Nutritional requirements (protein, vitamins, etc.)"
            },
            "Transportation": {
                "Description": "Minimize shipping costs from sources to destinations",
                "Variables": "Units shipped from each source to each destination",
                "Objective": "Minimize total transportation cost",
                "Constraints": "Supply limits and demand requirements"
            },
            "Assignment": {
                "Description": "Assign tasks to workers optimally",
                "Variables": "Binary variables (0 or 1) for assignments",
                "Objective": "Minimize total cost or maximize efficiency",
                "Constraints": "Each task assigned to exactly one worker"
            }
        }
        
        for prob_type, details in problem_types.items():
            with st.expander(f"📋 {prob_type} Problems"):
                st.markdown(f"**Description:** {details['Description']}")
                st.markdown(f"**Decision Variables:** {details['Variables']}")
                st.markdown(f"**Objective:** {details['Objective']}")
                st.markdown(f"**Typical Constraints:** {details['Constraints']}")
    
    with tab4:
        st.subheader("Common Mistakes and How to Avoid Them")
        
        mistakes = [
            {
                "mistake": "Forgetting non-negativity constraints",
                "consequence": "May get negative solutions that don't make sense",
                "solution": "Always include xᵢ ≥ 0 for all variables unless negative values are meaningful"
            },
            {
                "mistake": "Wrong constraint direction (≤ vs ≥)",
                "consequence": "Incorrect feasible region, wrong optimal solution",
                "solution": "Carefully read problem: 'at most' = ≤, 'at least' = ≥"
            },
            {
                "mistake": "Inconsistent units in constraints",
                "consequence": "Mathematical errors, meaningless solutions",
                "solution": "Ensure all coefficients use the same units (e.g., hours, dollars)"
            },
            {
                "mistake": "Mixing maximization and minimization",
                "consequence": "Incorrect objective value interpretation",
                "solution": "Be clear about problem type; convert if needed (min f = max -f)"
            },
            {
                "mistake": "Not checking solution feasibility",
                "consequence": "Implementing infeasible or suboptimal solutions",
                "solution": "Always verify final solution satisfies all original constraints"
            }
        ]
        
        for i, item in enumerate(mistakes, 1):
            st.markdown(f"**{i}. {item['mistake']}**")
            st.markdown(f"❌ **Problem:** {item['consequence']}")
            st.markdown(f"✅ **Solution:** {item['solution']}")
            st.markdown("---")

if __name__ == "__main__":
    main()
