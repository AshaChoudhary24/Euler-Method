import math
import matplotlib.pyplot as plt

# Safe math environment for evaluating expressions like "x + y", "sin(x)", "e**x"
SAFE_MATH = {
    'sin': math.sin,
    'cos': math.cos,
    'tan': math.tan,
    'exp': math.exp,
    'log': math.log,
    'sqrt': math.sqrt,
    'pi': math.pi,
    'e': math.e,
}

def parse_derivative(expr_str):
    """Compiles a mathematical expression in terms of x and y into a callable function."""
    # Allow natural power notation (^) alongside Python (**)
    expr_clean = expr_str.replace('^', '**')
    compiled_expr = compile(expr_clean, '<string>', 'eval')

    def f(x, y):
        env = dict(SAFE_MATH)
        env['x'] = x
        env['y'] = y
        return eval(compiled_expr, {"__builtins__": {}}, env)

    return f

def get_float_input(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a valid real number.")

def get_int_input(prompt, min_val=1):
    while True:
        try:
            val = int(input(prompt))
            if val < min_val:
                print(f"Please enter an integer >= {min_val}.")
                continue
            return val
        except ValueError:
            print("Invalid input. Please enter an integer.")

def main():
    print("=" * 50)
    print("       Euler's Method Differential Equation Solver")
    print("=" * 50)
    print("Supported syntax: x, y, +, -, *, /, ** (or ^), sin(), cos(), exp(), log(), etc.")
    
    # 1. Differential Equation Input
    while True:
        expr_str = input("\nEnter dy/dx in terms of x and/or y (e.g., 'x + 2*y' or 'x^2 - y'): ").strip()
        try:
            f = parse_derivative(expr_str)
            # Test run at an arbitrary point to catch syntax errors early
            f(1.0, 1.0)
            break
        except Exception as err:
            print(f"Error parsing expression ({err}). Please check your syntax and retry.")

    # 2. Initial Condition
    print("\n--- Initial Condition ---")
    x0 = get_float_input("Enter initial x (x0): ")
    y0 = get_float_input("Enter initial y (y0): ")

    # 3. Step Specification (Choose 2 of: dx, steps, x_final)
    print("\n--- Step Parameters ---")
    print("Select which TWO parameters you want to provide:")
    print("  [1] Step size (dx) and Number of steps (n)")
    print("  [2] Step size (dx) and Final x-value (x_final)")
    print("  [3] Number of steps (n) and Final x-value (x_final)")

    while True:
        choice = input("Enter choice (1, 2, or 3): ").strip()
        if choice in {'1', '2', '3'}:
            break
        print("Invalid choice. Please select 1, 2, or 3.")

    if choice == '1':
        dx = get_float_input("Enter step size (dx): ")
        n = get_int_input("Enter number of steps (n): ")
        x_final = x0 + n * dx
    elif choice == '2':
        dx = get_float_input("Enter step size (dx): ")
        x_final = get_float_input("Enter final x (x_final): ")
        n = int(round((x_final - x0) / dx))
        if n <= 0:
            print(f"Warning: Computed {n} steps. Adjusting direction or values.")
            n = max(1, abs(n))
    elif choice == '3':
        n = get_int_input("Enter number of steps (n): ")
        x_final = get_float_input("Enter final x (x_final): ")
        dx = (x_final - x0) / n

    # 4. Run Euler's Method
    x_vals = [x0]
    y_vals = [y0]

    curr_x, curr_y = x0, y0
    for _ in range(n):
        try:
            slope = f(curr_x, curr_y)
        except ZeroDivisionError:
            print(f"\nMath Error: Division by zero at ({curr_x:.4f}, {curr_y:.4f}). Halting simulation.")
            break
        except Exception as e:
            print(f"\nEvaluation error at ({curr_x:.4f}, {curr_y:.4f}): {e}. Halting simulation.")
            break

        curr_y = curr_y + slope * dx
        curr_x = curr_x + dx
        x_vals.append(curr_x)
        y_vals.append(curr_y)

    # 5. Output Final Results
    print("\n" + "=" * 50)
    print("                   Results")
    print("=" * 50)
    print(f"Formula dy/dx : {expr_str}")
    print(f"Initial point : ({x0}, {y0})")
    print(f"Step size (dx): {dx:.6g}")
    print(f"Total steps   : {len(x_vals) - 1}")
    print(f"Final point   : ({x_vals[-1]:.6f}, {y_vals[-1]:.6f})")

    # Optional table print
    show_table = input("\nPrint full step-by-step table? (y/n): ").strip().lower()
    if show_table == 'y':
        print(f"\n{'Step':<6} {'x':<15} {'y':<15}")
        print("-" * 36)
        for i, (x_pt, y_pt) in enumerate(zip(x_vals, y_vals)):
            print(f"{i:<6} {x_pt:<15.6f} {y_pt:<15.6f}")

    # Optional graph plot
    show_plot = input("\nPlot the solution curve? (y/n): ").strip().lower()
    if show_plot == 'y':
        plt.figure(figsize=(8, 5))
        plt.plot(x_vals, y_vals, marker='o', markersize=3, linestyle='-', label=f"Euler approx (dx = {dx:.4g})")
        plt.plot(x0, y0, 'go', label=f"Start ({x0}, {y0})")
        plt.plot(x_vals[-1], y_vals[-1], 'ro', label=f"End ({x_vals[-1]:.4f}, {y_vals[-1]:.4f})")
        plt.title(f"Euler's Method for dy/dx = {expr_str}")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.legend()
        plt.tight_layout()
        plt.show()

if __name__ == '__main__':
    main()