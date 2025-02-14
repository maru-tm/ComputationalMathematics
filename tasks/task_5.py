import tkinter as tk
from tkinter import messagebox
import numpy as np
import sys
import os
from PIL import Image, ImageTk

# Добавляем путь к корню проекта
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from methods.curve_fitting import least_squares_fit  # Импорт метода наименьших квадратов
from utils.plotter import plot_function_graph  # Импорт функции для построения графика

IMAGE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../paper_based_solutions/task5_solution.jpg"))

class LinearCurveFittingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Task 5: Linear Curve Fitting")
        self.geometry("600x800")

        # Task description
        tk.Label(self, text="Task 5: Linear Curve Fitting", font=("Arial", 14, "bold")).pack(pady=5)
        tk.Label(self, text="Fit a line to data points using the Least Squares method.", font=("Arial", 12)).pack(pady=5)
        tk.Label(self, text="Default data points: (1,2), (2,3), (3,5), (4,7), (5,11)", font=("Arial", 12)).pack(pady=5)

        # Explanation
        explanation_text = (
            "The Least Squares method finds the line that minimizes the sum of squared vertical distances from "
            "the data points to the line. It is widely used in statistics and data analysis to fit a linear model to data."
        )
        tk.Label(self, text="Explanation of the Least Squares Method:", font=("Arial", 14, "bold")).pack(pady=5)
        tk.Label(self, text=explanation_text, justify="left", wraplength=550).pack(pady=5)

        # Input fields
        tk.Label(self, text="Enter x values (default: 1 2 3 4 5):").pack(pady=5)
        self.x_entry = tk.Entry(self, width=40)
        self.x_entry.insert(0, "1 2 3 4 5")
        self.x_entry.pack(pady=5)

        tk.Label(self, text="Enter y values (default: 2 3 5 7 11):").pack(pady=5)
        self.y_entry = tk.Entry(self, width=40)
        self.y_entry.insert(0, "2 3 5 7 11")
        self.y_entry.pack(pady=5)

        # Buttons
        tk.Button(self, text="Fit Line", command=self.fit_line).pack(pady=10)
        tk.Button(self, text="Show Graph", command=self.show_graph).pack(pady=5)
        tk.Button(self, text="Show Conclusion", command=self.show_conclusion).pack(pady=5)
        tk.Button(self, text="Show Solution Image", command=self.open_solution_image).pack(pady=5)

        # Result output
        self.result_label = tk.Label(self, text="", fg="blue", justify="left", wraplength=550)
        self.result_label.pack(pady=10)

    def fit_line(self):
        """Fit a line using the Least Squares method and display the result."""
        try:
            self.x = np.array(list(map(float, self.x_entry.get().split())), dtype=float)
            self.y = np.array(list(map(float, self.y_entry.get().split())), dtype=float)

            if len(self.x) != len(self.y):
                raise ValueError("x and y must have the same length.")

            self.a, self.b = least_squares_fit(self.x, self.y)
            result_text = f"Equation of the line: y = {self.a:.4f}x + {self.b:.4f}"
            self.result_label.config(text=result_text)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def show_graph(self):
        """Plot the fitted line."""
        try:
            if not hasattr(self, "a") or not hasattr(self, "b"):
                messagebox.showerror("Error", "Fit the line first!")
                return

            equation_str = f"{self.a} * x + {self.b}"
            plot_function_graph(equation_str, min(self.x) - 1, max(self.x) + 1,
                                title="Linear Approximation using Least Squares Method")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def show_conclusion(self):
        """Show the conclusion about the Least Squares method."""
        try:
            if not hasattr(self, "a") or not hasattr(self, "b"):
                messagebox.showerror("Error", "Fit the line first!")
                return

            conclusion_text = (
                "The Least Squares method successfully fitted a line to the given data points. The equation of the line is:\n\n"
                f"y = {self.a:.4f}x + {self.b:.4f}\n\n"
                "Strengths:\n"
                "- Simple to implement and widely used.\n"
                "- Provides a good approximation for linear relationships.\n\n"
                "Weaknesses:\n"
                "- Sensitive to outliers.\n"
                "- Assumes a linear relationship between variables.\n\n"
                "Recommendation:\n"
                "To improve accuracy, remove outliers from the data and ensure that the relationship is approximately linear."
            )
            messagebox.showinfo("Conclusion", conclusion_text)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def open_solution_image(self):
        """Open the solution image in a new window."""
        try:
            img = Image.open(IMAGE_PATH)
            img = ImageTk.PhotoImage(img)

            top = tk.Toplevel(self)
            top.title("Solution Image")
            label = tk.Label(top, image=img)
            label.image = img  # Keep a reference to the image
            label.pack()

        except Exception as e:
            messagebox.showerror("Error", f"Error opening image: {e}")

if __name__ == "__main__":
    app = LinearCurveFittingApp()
    app.mainloop()
