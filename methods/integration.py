import numpy as np

def trapezoidal_rule(f, a, b, n):
    """
    Numerical integration using the trapezoidal rule.

    :param f: Function f(x), the integrand
    :param a: Lower integration limit
    :param b: Upper integration limit
    :param n: Number of subdivisions (subintervals)
    :return: Approximate integral value
    """
    x = np.linspace(a, b, n + 1)  # Divide the interval
    y = f(x)  # Function values at the nodes
    h = (b - a) / n  # Step size

    integral = (h / 2) * (y[0] + 2 * sum(y[1:n]) + y[n])  # Trapezoidal rule formula
    return integral
