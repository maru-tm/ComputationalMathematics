import tkinter as tk
from tkinter import messagebox
import numpy as np
import sys
import os
from PIL import Image, ImageTk  # Не забудьте импортировать для работы с изображениями

# Добавляем путь к корню проекта
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from methods.jacobi import jacobi_method  # Импортируем метод Якоби

# Путь к изображению
IMAGE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../paper_based_solutions/task3_solution.jpg"))

class JacobiApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Task 3: Jacobi Method")
        self.geometry("600x600")

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
        tk.Label(scrollable_frame, text="Task 3: Jacobi Method Solver", font=("Arial", 14, "bold")).pack(pady=5)
        tk.Label(scrollable_frame, text="Solve the system of linear equations using the Jacobi Method.", font=("Arial", 12)).pack(pady=5)
        tk.Label(scrollable_frame, text="Initial System (default):", font=("Arial", 12)).pack()
        tk.Label(scrollable_frame, text="2x + y + z = 5\n y + 2z = -1\n 2x + y + 3z = 8", font=("Arial", 12)).pack(pady=5)

        # Explanation
        tk.Label(scrollable_frame, text="Explanation", font=("Arial", 14, "bold")).pack(pady=5)
        explanation_text = (
            "1. **Jacobi Method:**\n"
            "   - Rearrange each equation to isolate one variable.\n"
            "   - Start with an initial guess (e.g., [0, 0, 0]).\n"
            "   - Iteratively update the values using the previous approximation.\n"
            "   - Stop when the difference between iterations is below a specified tolerance.\n\n"
            "   Formulae for the given system:\n"
            "   - x = (5 - y - z) / 2\n"
            "   - y = (-1 - z) / 2\n"
            "   - z = (8 - 2x - y) / 3"
        )
        tk.Label(scrollable_frame, text=explanation_text, justify="left", wraplength=550).pack(pady=5)

        # Input Fields
        tk.Label(scrollable_frame, text="Enter initial guess (x0, y0, z0):").pack(pady=5)
        self.initial_guess_entry = tk.Entry(scrollable_frame, width=40)
        self.initial_guess_entry.insert(0, "0 0 0")
        self.initial_guess_entry.pack(pady=5)

        tk.Label(scrollable_frame, text="Max Iterations:").pack(pady=5)
        self.max_iter_entry = tk.Entry(scrollable_frame, width=10)
        self.max_iter_entry.insert(0, "100")
        self.max_iter_entry.pack(pady=5)

        tk.Label(scrollable_frame, text="Tolerance:").pack(pady=5)
        self.tolerance_entry = tk.Entry(scrollable_frame, width=10)
        self.tolerance_entry.insert(0, "1e-6")
        self.tolerance_entry.pack(pady=5)

        # Buttons
        tk.Button(scrollable_frame, text="Solve System", command=self.solve_system).pack(pady=10)
        tk.Button(scrollable_frame, text="Show Conclusion", command=self.show_conclusion).pack(pady=5)
        tk.Button(scrollable_frame, text="Open Solution Image", command=self.open_solution_image).pack(pady=10)  # Новая кнопка для изображения

        # Result Output
        self.result_label = tk.Label(scrollable_frame, text="", fg="blue", justify="left", wraplength=550)
        self.result_label.pack(pady=10)

    def solve_system(self):
        """Solve the system using the Jacobi Method."""
        try:
            # Updated system of equations
            A = np.array([
                [2, 1, 1],
                [0, 2, 1],
                [2, 1, 3]
            ], dtype=float)
            B = np.array([5, -1, 8], dtype=float)

            # Get user inputs
            initial_guess = list(map(float, self.initial_guess_entry.get().split()))
            max_iter = int(self.max_iter_entry.get())
            tolerance = float(self.tolerance_entry.get())

            # Solve the system using Jacobi method
            solution, iterations = jacobi_method(A, B, x0=initial_guess, tol=tolerance, max_iterations=max_iter)

            result_text = (
                f"Solution Found:\n"
                f"x = {solution[0]:.5f}\n"
                f"y = {solution[1]:.5f}\n"
                f"z = {solution[2]:.5f}\n\n"
                f"Converged in {iterations} iterations."
            )
            self.result_label.config(text=result_text)

            # Store results for conclusion
            self.solution = solution
            self.iterations = iterations

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def show_conclusion(self):
        """Show the conclusion about the Jacobi method."""
        try:
            if not hasattr(self, "solution"):
                messagebox.showerror("Error", "Solve the system first!")
                return

            conclusion_text = (
                f"**Conclusion:**\n\n"
                f"The Jacobi method successfully solved the system of equations. "
                f"The solution was found in {self.iterations} iterations.\n\n"
                f"**Strengths:**\n"
                f"- Easy to implement.\n"
                f"- Can be parallelized.\n\n"
                f"**Weaknesses:**\n"
                f"- May not converge if the system is not diagonally dominant.\n"
                f"- Slower convergence compared to other methods like Gauss-Seidel.\n\n"
                f"**Recommendation:**\n"
                f"To ensure convergence, verify that the matrix is diagonally dominant."
            )
            messagebox.showinfo("Conclusion", conclusion_text)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

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

if __name__ == "__main__":
    app = JacobiApp()
    app.mainloop()
