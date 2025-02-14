import numpy as np

def newtons_forward_derivative(x, y, x_target):
    """
    Computes the first derivative using Newton's finite difference method.

    :param x: Interpolation nodes
    :param y: Function values at nodes
    :param x_target: Point at which the derivative is to be estimated
    :return: Approximate value of dy/dx at x_target
    """
    n = len(x)
    if n < 2:
        raise ValueError("At least two nodes are required to compute the derivative.")

    h = x[1] - x[0]  # Step size
    diff_table = np.zeros((n, n))
    diff_table[:, 0] = y

    # Compute finite differences
    for j in range(1, n):
        for i in range(n - j):
            diff_table[i][j] = diff_table[i + 1][j - 1] - diff_table[i][j - 1]

    # Compute derivative
    p = (x_target - x[0]) / h  # Relative position of the point
    derivative = diff_table[0][1] / h

    # Include higher-order differences
    term = 1
    for j in range(2, n):
        term *= (p - (j - 2)) / j
        derivative += term * diff_table[0][j] / h

    return derivative
