import tkinter as tk
from tkinter import messagebox, scrolledtext
from PIL import Image, ImageTk
import numpy as np
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from methods.interpolation import newtons_forward_interpolation

TASK_DESCRIPTION = """Task 6: Newton’s Forward Interpolation Formula
Problem: Given data points x=[0,1,2,3] and y=[1,4,9,16], estimate f(1.5).
"""

SOLUTION_EXPLANATION = """Solution Explanation:
1. **Use Newton’s Forward Interpolation Formula** to approximate f(x).
2. **Construct the forward difference table** based on given data points.
3. **Use the formula** to estimate f(x_interp).
"""

TEST_CASES = """Other Test Cases:
1. x=[0,2,4,6], y=[1,4,9,16] → f(3)
2. x=[1,2,3,4], y=[2,5,10,17] → f(2.5)
3. x=[0, π/4, π/2], y=[0, 0.707, 1] → f(π/6)
"""

IMAGE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../paper_based_solutions/task6_solution.jpg"))

class InterpolationApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Task 5: Newton’s Forward Interpolation Formula")
        self.geometry("700x500")

        # Scrollable frame
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        canvas = tk.Canvas(container)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Task Description
        tk.Label(scrollable_frame, text="Task Description", font=("Arial", 12, "bold")).pack(pady=5)
        tk.Label(scrollable_frame, text=TASK_DESCRIPTION, wraplength=650, justify="left").pack(pady=5)

        # Solution Explanation
        tk.Label(scrollable_frame, text="Solution Explanation", font=("Arial", 12, "bold")).pack(pady=5)
        tk.Label(scrollable_frame, text=SOLUTION_EXPLANATION, wraplength=650, justify="left").pack(pady=5)

        # Test Cases
        tk.Label(scrollable_frame, text="Other Test Cases", font=("Arial", 12, "bold")).pack(pady=5)
        tk.Label(scrollable_frame, text=TEST_CASES, wraplength=650, justify="left").pack(pady=5)

        # Input Fields
        tk.Label(scrollable_frame, text="Enter x points (comma separated):").pack(pady=5)
        self.x_entry = tk.Entry(scrollable_frame, width=50)
        self.x_entry.insert(0, "0,1,2,3")
        self.x_entry.pack(pady=5)

        tk.Label(scrollable_frame, text="Enter y values (comma separated):").pack(pady=5)
        self.y_entry = tk.Entry(scrollable_frame, width=50)
        self.y_entry.insert(0, "1,4,9,16")
        self.y_entry.pack(pady=5)

        tk.Label(scrollable_frame, text="Enter interpolation point:").pack(pady=5)
        self.x_interp_entry = tk.Entry(scrollable_frame, width=20)
        self.x_interp_entry.insert(0, "1.5")
        self.x_interp_entry.pack(pady=5)

        # Buttons
        self.calc_button = tk.Button(scrollable_frame, text="Calculate", command=self.calculate_interpolation)
        self.calc_button.pack(pady=5)

        # Scrollable Output Field
        tk.Label(scrollable_frame, text="Result:", font=("Arial", 12, "bold")).pack(pady=5)
        self.result_text = scrolledtext.ScrolledText(scrollable_frame, width=80, height=5, wrap=tk.WORD)
        self.result_text.pack(pady=5)

        # Button to show image
        self.image_button = tk.Button(scrollable_frame, text="Show Solution Image", command=self.show_image)
        self.image_button.pack(pady=10)

    def calculate_interpolation(self):
        """Computes the interpolated value."""
        try:
            x_values = np.array(list(map(float, self.x_entry.get().split(","))))
            y_values = np.array(list(map(float, self.y_entry.get().split(","))))
            x_interp = float(self.x_interp_entry.get())

            result = newtons_forward_interpolation(x_values, y_values, x_interp)

            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"Value of f({x_interp}) ≈ {result:.4f}\n")

        except ValueError:
            messagebox.showerror("Error", "Invalid numerical input!")

    def show_image(self):
        """Opens the solution image in a new window."""
        if not os.path.exists(IMAGE_PATH):
            messagebox.showerror("Error", f"Image not found:\n{IMAGE_PATH}")
            return

        img_window = tk.Toplevel(self)
        img_window.title("Solution Image")

        img = Image.open(IMAGE_PATH)
        img = img.resize((500, 400), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(img)

        img_label = tk.Label(img_window, image=photo)
        img_label.image = photo  # Keep reference
        img_label.pack()

if __name__ == "__main__":
    app = InterpolationApp()
    app.mainloop()
