import numpy as np

def iterative_matrix_inverse(A, tol=1e-6, max_iterations=100):
    """
    Iterative method for finding the inverse of a matrix (Newton-Schulz method).

    :param A: Square matrix (numpy.array)
    :param tol: Tolerance (default: 1e-6)
    :param max_iterations: Maximum number of iterations
    :return: Inverse matrix A_inv
    """
    n = A.shape[0]
    I = np.eye(n)

    # Initial approximation: A^T / Tr(A^T A)
    X = A.T / np.trace(A.T @ A)

    for _ in range(max_iterations):
        X_new = X @ (2 * I - A @ X)
        if np.linalg.norm(A @ X_new - I, ord=np.inf) < tol:
            return X_new
        X = X_new

    raise ValueError("The method did not converge within the given number of iterations")
