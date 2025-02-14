import numpy as np

def is_diagonally_dominant(A):
    """Проверяет, является ли матрица диагонально доминирующей."""
    for i in range(len(A)):
        if abs(A[i][i]) < sum(abs(A[i][j]) for j in range(len(A)) if j != i):
            return False
    return True

def jacobi_method(A, b, x0=None, tol=1e-6, max_iterations=100):
    n = len(b)
    x = np.zeros(n) if x0 is None else np.array(x0, dtype=float)
    x_new = np.zeros(n)

    # Проверка на диагональное преобладание
    # if not is_diagonally_dominant(A):
    #     raise ValueError("Матрица A не является диагонально доминирующей! Метод Якоби может не сходиться.")

    for iteration in range(max_iterations):
        for i in range(n):
            sum_ = sum(A[i][j] * x[j] for j in range(n) if j != i)
            x_new[i] = (b[i] - sum_) / A[i][i]

        if np.linalg.norm(x_new - x, ord=np.inf) < tol:
            return x_new, iteration + 1

        x = x_new.copy()

    raise ValueError("Jacobi method did not converge within the given number of iterations")
