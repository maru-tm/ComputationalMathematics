import tkinter as tk
from tkinter import ttk

def show_conclusion(master, root_bisection, iter_bisec, root_secant, iter_sec):
    """Creates a popup with comparison results"""
    win = tk.Toplevel(master)
    win.title("Conclusion")
    win.geometry("800x600")

    relative_error = abs((root_secant - root_bisection) / root_bisection) * 100

    # Таблица сравнения
    columns = ("Method", "Root", "Iterations")
    tree = ttk.Treeview(win, columns=columns, show="headings")
    tree.heading("Method", text="Method")
    tree.heading("Root", text="Root")
    tree.heading("Iterations", text="Iterations")

    tree.insert("", "end", values=("Bisection", f"{root_bisection:.5f}", iter_bisec))
    tree.insert("", "end", values=("Secant", f"{root_secant:.5f}", iter_sec))

    tree.pack(pady=10)

    # Анализ
    conclusion_text = (
        f"Bisection method required {iter_bisec} iterations to find {root_bisection:.5f}.\n"
        f"Secant method found {root_secant:.5f} in {iter_sec} iterations.\n\n"
        f"The Secant method converged faster, but requires good initial guesses.\n"
        f"The relative error between the two methods is {relative_error:.5f}%."
    )

    tk.Label(win, text=conclusion_text, justify="left", wraplength=450).pack(pady=10)
    tk.Button(win, text="Close", command=win.destroy).pack(pady=5)
