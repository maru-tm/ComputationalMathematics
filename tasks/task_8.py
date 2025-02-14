import sys
import os
import numpy as np
import tkinter as tk
from tkinter import messagebox, scrolledtext, Toplevel
from PIL import Image, ImageTk  # Для работы с изображениями

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from methods.integration import trapezoidal_rule
from utils.plotter import plot_function_graph  # Убедись, что у тебя есть эта функция

TASK_DESCRIPTION = """Task 8: Trapezoidal Rule
Problem: Approximate ∫[0,1] (x² + x) dx using the Trapezoidal Rule with 4 subintervals.
Compare the result with the exact integral value.
"""

SOLUTION_EXPLANATION = """Solution Explanation:
1. **Trapezoidal Rule Formula**:
   ∫[a,b] f(x) dx ≈ (h/2) * [f(a) + 2*f(x1) + 2*f(x2) + ... + 2*f(xn-1) + f(b)]
   where h = (b-a)/n is the step size.

2. **Compute function values at subintervals**.
3. **Sum up the contributions using the formula**.
4. **Compare with the exact integral value**.
"""

TEST_CASES = """Other Test Cases:
1. ∫[1,3] (2x + 3) dx with n=6
2. ∫[0,2] sin(x) dx with n=10
3. ∫[0, π] cos(x) dx with n=8
"""

# Путь к изображению для задачи 8
IMAGE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../paper_based_solutions/task8_solution.jpg"))

class IntegrationApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Task 8: Trapezoidal Rule")
        self.geometry("600x600")

        # Контейнер с прокруткой
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

        # Ввод функции
        tk.Label(scrollable_frame, text="Enter function f(x):").pack(pady=5)
        self.func_entry = tk.Entry(scrollable_frame, width=40)
        self.func_entry.insert(0, "x**2 + x")
        self.func_entry.pack(pady=5)

        # Ввод пределов интегрирования
        tk.Label(scrollable_frame, text="Lower limit (a):").pack()
        self.a_entry = tk.Entry(scrollable_frame, width=10)
        self.a_entry.insert(0, "0")
        self.a_entry.pack()

        tk.Label(scrollable_frame, text="Upper limit (b):").pack()
        self.b_entry = tk.Entry(scrollable_frame, width=10)
        self.b_entry.insert(0, "1")
        self.b_entry.pack()

        # Ввод числа разбиений
        tk.Label(scrollable_frame, text="Number of subintervals (n):").pack()
        self.n_entry = tk.Entry(scrollable_frame, width=10)
        self.n_entry.insert(0, "4")
        self.n_entry.pack()

        # Кнопка вычисления
        tk.Button(scrollable_frame, text="Calculate", command=self.solve).pack(pady=10)

        # Кнопка для построения графика
        tk.Button(scrollable_frame, text="Plot Graph", command=self.plot_graph).pack(pady=5)

        # Вывод результатов с прокруткой
        tk.Label(scrollable_frame, text="Result:", font=("Arial", 12, "bold")).pack(pady=5)
        self.result_text = scrolledtext.ScrolledText(scrollable_frame, width=60, height=5, wrap=tk.WORD)
        self.result_text.pack(pady=5)

        # Test cases
        tk.Label(scrollable_frame, text="Other Test Cases:", font=("Arial", 12, "bold")).pack(pady=5)
        tk.Label(scrollable_frame, text=TEST_CASES, wraplength=550, justify="left").pack(pady=5)

        # Кнопка для открытия изображения
        tk.Button(scrollable_frame, text="View Solution Image", command=self.open_image).pack(pady=10)

    def solve(self):
        try:
            # Получаем вводные данные
            func_str = self.func_entry.get()
            a = float(self.a_entry.get())
            b = float(self.b_entry.get())
            n = int(self.n_entry.get())

            # Создаем функцию f(x) для использования в коде
            local_dict = {"np": np}
            f = lambda x: eval(func_str, {"x": x, "np": np}, local_dict)

            # Вычисляем интеграл
            approx_integral = trapezoidal_rule(f, a, b, n)

            # Вычисляем точное значение аналитически (если возможно)
            exact_integral = (b**3 / 3 + b**2 / 2) - (a**3 / 3 + a**2 / 2)

            # Выводим результат в UI
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, (
                f"Approximate integral: {approx_integral:.6f}\n"
                f"Exact integral: {exact_integral:.6f}\n"
                f"Error: {abs(exact_integral - approx_integral):.6f}"
            ))

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def plot_graph(self):
        try:
            func_str = self.func_entry.get()
            a = float(self.a_entry.get())
            b = float(self.b_entry.get())

            local_dict = {"np": np}

            plot_function_graph(func_str, a, b, title="Function Graph")

        except Exception as e:
            messagebox.showerror("Error", f"Error plotting graph: {e}")

    def open_image(self):
        """Открывает изображение с решением задачи 8."""
        image_window = Toplevel(self)
        image_window.title("Task 8 Solution Image")

        # Открытие изображения с использованием Pillow
        img = Image.open(IMAGE_PATH)
        img = ImageTk.PhotoImage(img)

        img_label = tk.Label(image_window, image=img)
        img_label.image = img  # Сохраняем ссылку на изображение
        img_label.pack()

if __name__ == "__main__":
    app = IntegrationApp()
    app.mainloop()
