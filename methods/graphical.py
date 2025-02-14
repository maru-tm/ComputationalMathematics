import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
from utils.plotter import plot_function_graph

def parse_function(func_str):
    """Парсит строку и возвращает вычисляемую функцию."""
    def f(x):
        try:
            return eval(func_str, {"x": x, "np": np})
        except Exception:
            return np.nan
    return f

def find_roots_graphically(func_str, x_min=0, x_max=3):
    """Находит все корни графическим методом."""
    f = parse_function(func_str)
    x_values = np.linspace(x_min, x_max, 1000)
    y_values = np.vectorize(f)(x_values)

    if np.isnan(y_values).any():
        print("Ошибка: некорректная функция")
        return None

    # Находим индексы, где функция меняет знак (корни)
    sign_changes = np.where(np.diff(np.sign(y_values)))[0]
    approx_roots = [fsolve(f, x_values[i])[0] for i in sign_changes]

    # Фильтруем корни, оставляя только те, что внутри [x_min, x_max]
    approx_roots = [root for root in approx_roots if x_min <= root <= x_max]

    # Строим график с отмеченными корнями
    # plot_function_graph(func_str, x_min, x_max, f"График функции: {func_str}", roots=approx_roots)

    return approx_roots

def calculate_absolute_errors(func_str, approx_roots):
    """Вычисляет абсолютные ошибки для всех найденных корней."""
    f = parse_function(func_str)
    errors = []
    
    for root in approx_roots:
        try:
            exact_root = fsolve(f, root)[0]  # Уточняем корень
            if np.isnan(exact_root):
                raise ValueError("Не удалось найти точный корень.")
            abs_error = abs(exact_root - root)
            errors.append((exact_root, abs_error))
        except Exception:
            print(f"Ошибка при нахождении точного корня для {root}.")
            errors.append((None, None))
    
    return errors
