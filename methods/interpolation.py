import numpy as np

def newtons_forward_interpolation(x, y, x_interp):
    """
    Newton's forward interpolation for equally spaced nodes.

    :param x: Interpolation nodes
    :param y: Function values at nodes
    :param x_interp: Point at which f(x) needs to be estimated
    :return: Interpolated value f(x_interp)
    """
    n = len(x)
    diff_table = np.zeros((n, n))
    diff_table[:, 0] = y

    # Compute forward differences
    for j in range(1, n):
        for i in range(n - j):
            diff_table[i][j] = diff_table[i + 1][j - 1] - diff_table[i][j - 1]

    # Compute the interpolated value at x_interp
    h = x[1] - x[0]  # Step size
    p = (x_interp - x[0]) / h  # Relative position of the point
    result = y[0]
    term = 1

    for j in range(1, n):
        term *= (p - (j - 1)) / j
        result += term * diff_table[0][j]

    return result
