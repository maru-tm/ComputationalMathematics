import numpy as np

def least_squares_fit(x, y):
    """
    Computes the coefficients a and b for the equation y = ax + b using the least squares method.
    
    :param x: Array of x values
    :param y: Array of y values
    :return: Coefficients a and b
    """
    n = len(x)
    sum_x = np.sum(x)
    sum_y = np.sum(y)
    sum_x2 = np.sum(x**2)
    sum_xy = np.sum(x * y)

    a = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x**2)
    b = (sum_y - a * sum_x) / n

    return a, b
