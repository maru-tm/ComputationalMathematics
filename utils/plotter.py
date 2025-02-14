import numpy as np
import matplotlib.pyplot as plt
def plot_function_graph(f, x_min, x_max, title="Function Graph", roots=None):
    """Строит график функции и отмечает найденные корни."""
    try:
        x_values = np.linspace(x_min, x_max, 1000)
        func = lambda x: eval(f, {"x": x, "np": np}) if isinstance(f, str) else f
        y_values = np.vectorize(func)(x_values)

        plt.figure(figsize=(8, 6))
        plt.axhline(0, color='black', linewidth=0.5)
        plt.axvline(0, color='black', linewidth=0.5)
        plt.plot(x_values, y_values, label="f(x)", color="blue")

        # Отмечаем все найденные корни
        if roots:
            plt.scatter(roots, [0] * len(roots), color='red', zorder=3, label="Найденные корни")

        plt.xlabel("x")
        plt.ylabel("f(x)")
        plt.legend()
        plt.title(title)
        plt.grid()
        plt.show()

    except Exception as e:
        print(f"Ошибка при построении графика: {e}")
