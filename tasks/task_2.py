import tkinter as tk
from tkinter import messagebox
import numpy as np
import sys
import os
from PIL import Image, ImageTk

# Добавляем путь к корню проекта
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from methods.root_finding import bisection_method, secant_method
from utils.plotter import plot_function_graph
from utils.conclusion_task2 import show_conclusion

IMAGE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../paper_based_solutions/task2_solution.jpg"))

class RootFindingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Task 2: Comparison of Root-Finding Methods")
        self.geometry("600x500")

        # Инициализация переменных для хранения результатов
        self.root_bisection = None
        self.iter_bisec = None
        self.root_secant = None
        self.iter_sec = None

        # Добавляем скроллинг к главному окну
        main_frame = tk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(main_frame)
        scrollbar = tk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        # Task Description
        tk.Label(scrollable_frame, text="Task 2: Comparison of Root-Finding Methods", font=("Arial", 14, "bold")).pack(pady=5)
        tk.Label(scrollable_frame, text="Find the root of f(x) = x² - 5 in the interval [2,3] using:", font=("Arial", 12)).pack()
        tk.Label(scrollable_frame, text="- Bisection method\n- Secant method\n- Measure iterations and calculate relative errors", font=("Arial", 12)).pack(pady=5)

        # Explanation
        tk.Label(scrollable_frame, text="Explanation", font=("Arial", 14, "bold")).pack(pady=5)
        explanation_text = (
            "1. **Bisection Method:**\n"
            "   - If f(a) and f(b) have opposite signs, the function has a root in [a, b].\n"
            "   - Compute the midpoint: c = (a + b) / 2.\n"
            "   - Replace either a or b with c depending on f(c).\n"
            "   - Stop when the interval is small enough.\n\n"
            "   Formula: cₙ = (aₙ + bₙ) / 2\n\n"
            "2. **Secant Method:**\n"
            "   - Uses two points (x₀, x₁) and the secant line to approximate the root.\n"
            "   - Update the next approximation using:\n"
            "     xₙ₊₁ = xₙ - f(xₙ) * (xₙ - xₙ₋₁) / (f(xₙ) - f(xₙ₋₁))\n"
            "   - Faster than bisection but requires good initial guesses.\n\n"
            "3. **Relative Error Calculation:**\n"
            "   - Error = |(exact - approx) / exact| * 100%\n"
        )
        tk.Label(scrollable_frame, text=explanation_text, justify="left", wraplength=550).pack(pady=5)

        # Other Test Functions
        tk.Label(scrollable_frame, text="Other Test Functions", font=("Arial", 14, "bold")).pack(pady=5)
        test_functions = (
            "1) f(x) = x³ - 4x + 1\n"
            "2) f(x) = sin(x) - 0.5\n"
            "3) f(x) = e^x - 2\n"
            "4) f(x) = log(x) - 1\n"
            "5) f(x) = x⁵ - 3x + 2"
        )
        tk.Label(scrollable_frame, text=test_functions, justify="left").pack(pady=5)

        # Input Fields
        tk.Label(scrollable_frame, text="Enter function f(x):").pack(pady=5)
        self.func_entry = tk.Entry(scrollable_frame, width=40)
        self.func_entry.insert(0, "x**2 - 5")
        self.func_entry.pack(pady=5)

        tk.Label(scrollable_frame, text="Left boundary (a):").pack(pady=5)
        self.a_entry = tk.Entry(scrollable_frame, width=10)
        self.a_entry.insert(0, "2")
        self.a_entry.pack(pady=5)

        tk.Label(scrollable_frame, text="Right boundary (b):").pack(pady=5)
        self.b_entry = tk.Entry(scrollable_frame, width=10)
        self.b_entry.insert(0, "3")
        self.b_entry.pack(pady=5)

        # Method Selection
        self.method_var = tk.StringVar(value="3")
        tk.Label(scrollable_frame, text="Select Method:").pack(pady=5)
        tk.Radiobutton(scrollable_frame, text="Bisection Method", variable=self.method_var, value="1").pack()
        tk.Radiobutton(scrollable_frame, text="Secant Method", variable=self.method_var, value="2").pack()
        tk.Radiobutton(scrollable_frame, text="Both Methods", variable=self.method_var, value="3").pack()

        # Buttons
        tk.Button(scrollable_frame, text="Calculate", command=self.solve).pack(pady=10)
        tk.Button(scrollable_frame, text="Plot Graph", command=self.plot_graph).pack(pady=5)
        tk.Button(scrollable_frame, text="Show Conclusion", command=self.show_conclusion).pack(pady=5)
        tk.Button(scrollable_frame, text="Open Solution Image", command=self.open_solution_image).pack(pady=5)

        # Result Output
        self.result_label = tk.Label(scrollable_frame, text="", fg="blue", justify="left", wraplength=550)
        self.result_label.pack(pady=10)

    def solve(self):
        try:
            func_str = self.func_entry.get()
            a = float(self.a_entry.get())
            b = float(self.b_entry.get())

            # Create lambda function
            local_dict = {"np": np}
            func = lambda x: eval(func_str, {"x": x}, local_dict)

            method_choice = self.method_var.get()
            result_text = ""

            if method_choice == "1":
                self.root_bisection, self.iter_bisec = bisection_method(func, a, b)
                result_text = f"Bisection Method:\nRoot: {self.root_bisection:.5f}, Iterations: {self.iter_bisec}"
            elif method_choice == "2":
                self.root_secant, self.iter_sec = secant_method(func, a, b)
                result_text = f"Secant Method:\nRoot: {self.root_secant:.5f}, Iterations: {self.iter_sec}"
            elif method_choice == "3":
                self.root_bisection, self.iter_bisec = bisection_method(func, a, b)
                self.root_secant, self.iter_sec = secant_method(func, a, b)
                relative_error = abs((self.root_secant - self.root_bisection) / self.root_bisection) * 100

                result_text = (
                    f"Bisection Method:\nRoot: {self.root_bisection:.5f}, Iterations: {self.iter_bisec}\n\n"
                    f"Secant Method:\nRoot: {self.root_secant:.5f}, Iterations: {self.iter_sec}\n\n"
                    f"Relative Error: {relative_error:.5f}%"
                )

            # Display result
            self.result_label.config(text=result_text)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def plot_graph(self):
        """Построить график функции с найденными корнями."""
        try:
            func_str = self.func_entry.get()  # Строка функции
            a = float(self.a_entry.get())
            b = float(self.b_entry.get())

            # Проверяем, были ли вычислены корни
            roots = []
            if self.method_var.get() in ["1", "3"] and self.root_bisection is not None:
                roots.append(float(self.root_bisection))
            if self.method_var.get() in ["2", "3"] and self.root_secant is not None:
                roots.append(float(self.root_secant))

            # Вызываем функцию построения графика с передачей строки
            if roots:
                plot_function_graph(func_str, a, b, roots=roots)
            else:
                messagebox.showwarning("Warning", "Сначала вычислите корни!")

        except Exception as e:
            messagebox.showerror("Error", f"Ошибка при построении графика: {e}")

    def open_solution_image(self):
        """Open the solution image in a new window."""
        try:
            img = Image.open(IMAGE_PATH)
            img = ImageTk.PhotoImage(img)  # Use the original size of the image

            top = tk.Toplevel(self)
            top.title("Solution Image")
            label = tk.Label(top, image=img)
            label.image = img  # Keep a reference to the image
            label.pack()

        except Exception as e:
            messagebox.showerror("Error", f"Error opening image: {e}")


    def show_conclusion(self):
        """Показать окно с сравнением методов"""
        try:
            if self.root_bisection is None or self.root_secant is None:
                messagebox.showerror("Error", "Calculate roots first!")
                return

            show_conclusion(self, self.root_bisection, self.iter_bisec, self.root_secant, self.iter_sec)

        except Exception as e:
            messagebox.showerror("Error", f"Error displaying conclusion: {e}")

if __name__ == "__main__":
    app = RootFindingApp()
    app.mainloop()
