import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import numpy as np
import sys
import os

# Добавляем путь к корню проекта
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from methods.matrix_inversion import iterative_matrix_inverse  # Импорт метода для итеративного вычисления обратной матрицы

# Путь к изображению с решением
IMAGE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../paper_based_solutions/task4_solution.jpg"))

class MatrixInversionApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Task 4: Iterative Method for Matrix Inversion")
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
        tk.Label(scrollable_frame, text="Task 4: Iterative Matrix Inversion", font=("Arial", 14, "bold")).pack(pady=5)
        tk.Label(scrollable_frame, text="Find the inverse of matrix A using an iterative method.", font=("Arial", 12)).pack(pady=5)
        tk.Label(scrollable_frame, text="Default matrix A:", font=("Arial", 12)).pack()
        tk.Label(scrollable_frame, text="4 -2 1\n-2 4 -2\n 1 -2 4", font=("Arial", 12)).pack(pady=5)

        # Explanation
        explanation_text = (
            "The iterative matrix inversion method finds the inverse of matrix A by:\n"
            "1. Making an initial guess (based on matrix trace).\n"
            "2. Iteratively refining the approximation until convergence is achieved.\n"
            "3. Convergence criteria depend on the tolerance."
        )
        tk.Label(scrollable_frame, text=explanation_text, justify="left", wraplength=550).pack(pady=5)

        # Input Fields
        tk.Label(scrollable_frame, text="Enter matrix row 1 (default: 4 -2 1):").pack(pady=5)
        self.row1_entry = tk.Entry(scrollable_frame, width=40)
        self.row1_entry.insert(0, "4 -2 1")
        self.row1_entry.pack(pady=5)

        tk.Label(scrollable_frame, text="Enter matrix row 2 (default: -2 4 -2):").pack(pady=5)
        self.row2_entry = tk.Entry(scrollable_frame, width=40)
        self.row2_entry.insert(0, "-2 4 -2")
        self.row2_entry.pack(pady=5)

        tk.Label(scrollable_frame, text="Enter matrix row 3 (default: 1 -2 4):").pack(pady=5)
        self.row3_entry = tk.Entry(scrollable_frame, width=40)
        self.row3_entry.insert(0, "1 -2 4")
        self.row3_entry.pack(pady=5)

        tk.Label(scrollable_frame, text="Max Iterations:").pack(pady=5)
        self.max_iter_entry = tk.Entry(scrollable_frame, width=10)
        self.max_iter_entry.insert(0, "100")
        self.max_iter_entry.pack(pady=5)

        tk.Label(scrollable_frame, text="Tolerance:").pack(pady=5)
        self.tolerance_entry = tk.Entry(scrollable_frame, width=10)
        self.tolerance_entry.insert(0, "1e-6")
        self.tolerance_entry.pack(pady=5)

        # Buttons
        tk.Button(scrollable_frame, text="Compute Inverse", command=self.compute_inverse).pack(pady=10)
        tk.Button(scrollable_frame, text="Show Conclusion", command=self.show_conclusion).pack(pady=5)
        tk.Button(scrollable_frame, text="Show Solution Image", command=self.open_solution_image).pack(pady=5)

        # Result Output
        self.result_label = tk.Label(scrollable_frame, text="", fg="blue", justify="left", wraplength=550)
        self.result_label.pack(pady=10)

    def compute_inverse(self):
        """Compute the inverse of the matrix using the iterative method."""
        try:
            # Получаем ввод пользователя
            row1 = list(map(float, self.row1_entry.get().split()))
            row2 = list(map(float, self.row2_entry.get().split()))
            row3 = list(map(float, self.row3_entry.get().split()))

            A = np.array([row1, row2, row3], dtype=float)

            max_iter = int(self.max_iter_entry.get())
            tolerance = float(self.tolerance_entry.get())

            # Вычисляем обратную матрицу
            A_inv = iterative_matrix_inverse(A, tol=tolerance, max_iterations=max_iter)

            result_text = "Inverse matrix:\n" + "\n".join([" ".join(f"{val:.5f}" for val in row) for row in A_inv])
            self.result_label.config(text=result_text)

            # Сохраняем результаты для вывода заключения
            self.A_inv = A_inv

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def show_conclusion(self):
        """Show the conclusion about the iterative matrix inversion method."""
        try:
            if not hasattr(self, "A_inv"):
                messagebox.showerror("Error", "Compute the inverse first!")
                return

            conclusion_text = (
                "The iterative method successfully computed the inverse matrix.\n\n"
                "Strengths:\n"
                "- Can be used for large matrices.\n"
                "- Convergence depends on matrix properties.\n\n"
                "Weaknesses:\n"
                "- May not converge for poorly conditioned matrices.\n"
                "- Requires a good initial guess for faster convergence."
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
    app = MatrixInversionApp()
    app.mainloop()
