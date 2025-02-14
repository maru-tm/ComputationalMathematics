import tkinter as tk
from tkinter import messagebox
import os
import subprocess

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Computational Mathematics Project - Variant 1")
        self.geometry("600x800")
        self.configure(bg="#f0f8ff")  # Light blue background for a soothing look

        # Project and course information
        tk.Label(self, text="Course: Computational Mathematics", font=("Arial", 16, "bold"), bg="#f0f8ff", fg="#2b3d52").pack(pady=5)
        tk.Label(self, text="Instructor: Keneskhanov Madiyar", font=("Arial", 12), bg="#f0f8ff", fg="#4a5d73").pack(pady=5)
        tk.Label(self, text="Group: SE-2327", font=("Arial", 12), bg="#f0f8ff", fg="#4a5d73").pack(pady=5)
        tk.Label(self, text="Team Members:", font=("Arial", 12, "bold"), bg="#f0f8ff", fg="#2b3d52").pack(pady=5)
        tk.Label(self, text=" - Berikzhan Alan", font=("Arial", 12), bg="#f0f8ff", fg="#4a5d73").pack()
        tk.Label(self, text=" - Marden Aruzhan", font=("Arial", 12), bg="#f0f8ff", fg="#4a5d73").pack()
        tk.Label(self, text=" - Sailauova Uldana", font=("Arial", 12), bg="#f0f8ff", fg="#4a5d73").pack()
        tk.Label(self, text="Variant: 1", font=("Arial", 12), bg="#f0f8ff", fg="#4a5d73").pack(pady=10)

        # Project introduction
        intro_text = (
            "This project contains solutions to various computational mathematics problems. "
            "Each task demonstrates a different numerical method or mathematical concept, implemented using Python."
        )
        tk.Label(self, text="Project Introduction:", font=("Arial", 14, "bold"), bg="#f0f8ff", fg="#2b3d52").pack(pady=5)
        tk.Label(self, text=intro_text, wraplength=550, justify="left", font=("Arial", 12), bg="#f0f8ff", fg="#4a5d73").pack(pady=5)

        # Task selection
        tk.Label(self, text="Select a Task:", font=("Arial", 14, "bold"), bg="#f0f8ff", fg="#2b3d52").pack(pady=10)

        # List of tasks with detailed descriptions
        tasks = [
            "Task 1: Graphical Method and Absolute Error",
            "Task 2: Comparison of Root-Finding Methods",
            "Task 3: Jacobi Method",
            "Task 4: Iterative Method for Matrix Inversion",
            "Task 5: Linear Curve Fitting",
            "Task 6: Newton’s Forward Interpolation Formula",
            "Task 7: First Derivative Using Newton’s Forward Difference Formula",
            "Task 8: Trapezoidal Rule"
        ]

        # Create buttons for each task
        for i, task in enumerate(tasks, start=1):
            btn = tk.Button(
                self,
                text=task,
                width=50,
                font=("Arial", 12),
                bg="#dceefb",  # Light blue button
                fg="#102a43",  # Dark blue text
                activebackground="#b3d4f8",  # Slightly darker on hover
                activeforeground="#102a43",  # Same text color on hover
                command=lambda num=i: self.run_task(num)
            )
            btn.pack(pady=5)

        # Exit button
        tk.Button(
            self,
            text="Exit",
            width=50,
            font=("Arial", 12, "bold"),
            bg="#f05454",  # Red background for exit
            fg="white",
            activebackground="#d43d3d",
            activeforeground="white",
            command=self.quit
        ).pack(pady=10)

    def run_task(self, task_num):
        """Run the selected task."""
        task_script = os.path.join("tasks", f"task_{task_num}.py")
        if os.path.exists(task_script):
            try:
                subprocess.Popen(["python", task_script], shell=True)  # Opens the task in a new window
            except Exception as e:
                messagebox.showerror("Error", f"Error running {task_script}:\n{e}")
        else:
            messagebox.showerror("Error", f"File {task_script} not found!")

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()