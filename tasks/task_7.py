import tkinter as tk
from tkinter import messagebox, scrolledtext
from PIL import Image, ImageTk
import numpy as np
import sys
import os
from tkinter import Toplevel, Label, PhotoImage

# Путь к изображению для задачи 7
IMAGE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../paper_based_solutions/task7_solution.jpg"))

# Добавляем корневую директорию проекта в путь
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from methods.differentiation import newtons_forward_derivative

TASK_DESCRIPTION = """Task 7: First Derivative Using Newton’s Forward Difference Formula
Problem: Given data points x=[0,1,2] and y=[1,8,27], estimate dy/dx at x=1.
"""

SOLUTION_EXPLANATION = """Solution Explanation:
1. **Use Newton’s Forward Difference Formula** to approximate the first derivative.
2. **Compute the divided differences** for the given data.
3. **Estimate dy/dx at x_target** using the first forward difference.
"""

TEST_CASES = """Other Test Cases:
1. x=[0,2,4,6], y=[1,4,9,16] → dy/dx at x=2
2. x=[1,2,3,4], y=[2,5,10,17] → dy/dx at x=3
3. x=[0, π/4, π/2], y=[0, 0.707, 1] → dy/dx at x=π/4
"""

class DerivativeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Task 7: First Derivative Using Newton’s Forward Difference Formula")
        self.geometry("600x550")

        # Создаем контейнер с прокруткой
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        canvas = tk.Canvas(container)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Task description
        tk.Label(scrollable_frame, text="Task Description", font=("Arial", 12, "bold")).pack(pady=5)
        tk.Label(scrollable_frame, text=TASK_DESCRIPTION, wraplength=550, justify="left").pack(pady=5)

        # Solution Explanation
        tk.Label(scrollable_frame, text="Solution Explanation", font=("Arial", 12, "bold")).pack(pady=5)
        tk.Label(scrollable_frame, text=SOLUTION_EXPLANATION, wraplength=550, justify="left").pack(pady=5)

        # Input fields
        tk.Label(scrollable_frame, text="Enter x values (space-separated):").pack(pady=5)
        self.x_entry = tk.Entry(scrollable_frame, width=50)
        self.x_entry.insert(0, "0 1 2")
        self.x_entry.pack(pady=5)

        tk.Label(scrollable_frame, text="Enter y values (space-separated):").pack(pady=5)
        self.y_entry = tk.Entry(scrollable_frame, width=50)
        self.y_entry.insert(0, "1 8 27")
        self.y_entry.pack(pady=5)

        tk.Label(scrollable_frame, text="Point to estimate dy/dx at:").pack(pady=5)
        self.x_target_entry = tk.Entry(scrollable_frame, width=10)
        self.x_target_entry.insert(0, "1")
        self.x_target_entry.pack(pady=5)

        # Calculate button
        self.calc_button = tk.Button(scrollable_frame, text="Calculate", command=self.calculate_derivative)
        self.calc_button.pack(pady=10)

        # Scrollable Output Field
        tk.Label(scrollable_frame, text="Result:", font=("Arial", 12, "bold")).pack(pady=5)
        self.result_text = scrolledtext.ScrolledText(scrollable_frame, width=60, height=5, wrap=tk.WORD)
        self.result_text.pack(pady=5)

        # Test cases
        tk.Label(scrollable_frame, text="Other Test Cases:", font=("Arial", 12, "bold")).pack(pady=5)
        tk.Label(scrollable_frame, text=TEST_CASES, wraplength=550, justify="left").pack(pady=5)

        # Image button
        self.image_button = tk.Button(scrollable_frame, text="Open Task 7 Solution Image", command=self.open_image)
        self.image_button.pack(pady=10)

    def calculate_derivative(self):
        """Вычисляет производную с использованием метода Ньютона."""
        try:
            # Читаем данные из полей ввода
            x_values = list(map(float, self.x_entry.get().split()))
            y_values = list(map(float, self.y_entry.get().split()))
            x_target = float(self.x_target_entry.get())

            # Проверка корректности ввода
            if len(x_values) != len(y_values):
                messagebox.showerror("Error", "Number of x and y values must be the same!")
                return

            # Вычисляем производную
            derivative = newtons_forward_derivative(np.array(x_values), np.array(y_values), x_target)

            # Выводим результат
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"Approximate dy/dx at x={x_target}: {derivative:.6f}")

        except ValueError:
            messagebox.showerror("Error", "Invalid numerical input!")

    
    # В методе open_image
    def open_image(self):
        """Открывает изображение с решением задачи 7."""
        image_window = Toplevel(self)
        image_window.title("Task 7 Solution Image")

        # Открытие изображения с использованием Pillow
        img = Image.open(IMAGE_PATH)
        img = ImageTk.PhotoImage(img)

        img_label = Label(image_window, image=img)
        img_label.image = img  # Сохраняем ссылку на изображение
        img_label.pack()

if __name__ == "__main__":
    app = DerivativeApp()
    app.mainloop()
