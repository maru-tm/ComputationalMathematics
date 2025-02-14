import numpy as np

def bisection_method(func, a, b, tol=1e-6, max_iter=100):
    """Bisection method for finding the root of a function"""
    if func(a) * func(b) >= 0:
        raise ValueError("Bisection method is not applicable: f(a) and f(b) must have opposite signs")

    iterations = 0
    while (b - a) / 2 > tol and iterations < max_iter:
        c = (a + b) / 2  # Midpoint of the interval
        if func(c) == 0:  # If the exact root is found
            break
        elif func(a) * func(c) < 0:
            b = c
        else:
            a = c
        iterations += 1

    return (a + b) / 2, iterations  # Return the root and the number of iterations

def secant_method(func, x0, x1, tol=1e-6, max_iter=100):
    """Secant method for finding the root of a function"""
    iterations = 0
    while abs(x1 - x0) > tol and iterations < max_iter:
        f_x0, f_x1 = func(x0), func(x1)
        if f_x1 - f_x0 == 0:  # Prevent division by zero
            break
        x_new = x1 - f_x1 * (x1 - x0) / (f_x1 - f_x0)  # Secant method formula
        x0, x1 = x1, x_new
        iterations += 1

    return x1, iterations  # Return the root and the number of iterations
