import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from methods.graphical import find_roots_graphically, calculate_absolute_errors
from utils.plotter import plot_function_graph

TASK_DESCRIPTION = """Task 1: Graphical Method and Absolute Error
Problem: 
Plot the graph of f(x) = x^3 - 4x + 1 in the range x ∈ [0,3]. 
Use the graph to find an approximate root and calculate the absolute error 
compared to the root found using a numerical method.
"""

SOLUTION_EXPLANATION = """Solution Explanation:
1. **Plot the Function:** We visualize f(x) = x^3 - 4x + 1 to identify where it crosses the x-axis.
2. **Find Approximate Roots:** We determine x-values where f(x) ≈ 0.
3. **Numerical Verification:** We use a numerical method (e.g., fsolve) to find the exact roots.
4. **Calculate Absolute Error:** We compute the difference between the graphical and numerical roots.
"""

TEST_FUNCTIONS = """Other Functions to Test:
1. f(x) = x^2 - 2
2. f(x) = sin(x) - 0.5
3. f(x) = exp(-x) - x
4. f(x) = x^5 - 3x^3 + x - 2
5. f(x) = cos(x) - x
"""

IMAGE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "paper_based_solutions", "task1_solution.jpg"))

class RootFindingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Task 1: Graphical Method and Absolute Error")
        self.geometry("700x700")

        # Scrollable Frame
        container = tk.Frame(self)
        canvas = tk.Canvas(container)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        container.pack(fill="both", expand=True)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Task Description
        tk.Label(self.scrollable_frame, text="Task Description", font=("Arial", 12, "bold")).pack(pady=5)
        tk.Label(self.scrollable_frame, text=TASK_DESCRIPTION, wraplength=650, justify="left").pack(pady=5)

        # Solution Explanation
        tk.Label(self.scrollable_frame, text="Solution Explanation", font=("Arial", 12, "bold")).pack(pady=5)
        tk.Label(self.scrollable_frame, text=SOLUTION_EXPLANATION, wraplength=650, justify="left").pack(pady=5)

        # Test Functions
        tk.Label(self.scrollable_frame, text="Other Test Functions", font=("Arial", 12, "bold")).pack(pady=5)
        tk.Label(self.scrollable_frame, text=TEST_FUNCTIONS, wraplength=650, justify="left").pack(pady=5)

        # Input Fields
        tk.Label(self.scrollable_frame, text="Enter f(x):").pack(pady=5)
        self.func_entry = tk.Entry(self.scrollable_frame, width=50)
        self.func_entry.insert(0, "x**3 - 4*x + 1")
        self.func_entry.pack(pady=5)

        tk.Label(self.scrollable_frame, text="Lower Bound (x_min):").pack(pady=5)
        self.x_min_entry = tk.Entry(self.scrollable_frame, width=10)
        self.x_min_entry.insert(0, "0")
        self.x_min_entry.pack(pady=5)

        tk.Label(self.scrollable_frame, text="Upper Bound (x_max):").pack(pady=5)
        self.x_max_entry = tk.Entry(self.scrollable_frame, width=10)
        self.x_max_entry.insert(0, "3")
        self.x_max_entry.pack(pady=5)

        # Buttons
        self.calc_button = tk.Button(self.scrollable_frame, text="Find Roots", command=self.calculate_roots)
        self.calc_button.pack(pady=5)

        self.plot_button = tk.Button(self.scrollable_frame, text="Plot Function", command=self.plot_graph)
        self.plot_button.pack(pady=5)

        # Output Field
        tk.Label(self.scrollable_frame, text="Results:", font=("Arial", 12, "bold")).pack(pady=5)
        self.result_text = tk.Text(self.scrollable_frame, width=80, height=10, wrap=tk.WORD)
        self.result_text.pack(pady=5)

        # Button to open image
        self.image_button = tk.Button(self.scrollable_frame, text="Open Solution Image", command=self.open_solution_image)
        self.image_button.pack(pady=10)

        self.canvas = canvas  # Store reference to canvas for resizing

    def calculate_roots(self):
        """Finds the approximate roots and calculates absolute errors."""
        try:
            func_str = self.func_entry.get()
            x_min = float(self.x_min_entry.get())
            x_max = float(self.x_max_entry.get())

            self.result_text.delete(1.0, tk.END)  # Clear previous results

            approx_roots = find_roots_graphically(func_str, x_min, x_max)
            if not approx_roots:
                self.result_text.insert(tk.END, "No roots found!\n")
                return

            errors = calculate_absolute_errors(func_str, approx_roots)

            result_text = "Found Roots:\n"
            for i, (approx, (exact, abs_err)) in enumerate(zip(approx_roots, errors), 1):
                result_text += f"{i}) Approximate: {approx:.5f}, Exact: {exact:.5f}, Error: {abs_err:.5e}\n"

            self.result_text.insert(tk.END, result_text)

        except ValueError:
            messagebox.showerror("Error", "Invalid numerical input!")

    def plot_graph(self):
        """Plots the function along with its approximate roots."""
        try:
            func_str = self.func_entry.get()
            x_min = float(self.x_min_entry.get())
            x_max = float(self.x_max_entry.get())

            approx_roots = find_roots_graphically(func_str, x_min, x_max)
            plot_function_graph(func_str, x_min, x_max, roots=approx_roots)

        except ValueError:
            messagebox.showerror("Error", "Invalid numerical input!")

    def open_solution_image(self):
        """Opens the solution image."""
        if not os.path.exists(IMAGE_PATH):
            messagebox.showerror("Error", f"Image not found: {IMAGE_PATH}")
            return

        img_window = tk.Toplevel(self)
        img_window.title("Solution Image")

        img = Image.open(IMAGE_PATH)
        img = img.resize((600, 400), Image.Resampling.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)

        label = tk.Label(img_window, image=img_tk)
        label.image = img_tk
        label.pack()

if __name__ == "__main__":
    app = RootFindingApp()
    app.mainloop()
