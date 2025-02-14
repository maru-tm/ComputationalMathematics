def relative_error(true_value, approx_value):
    """Вычисляет относительную ошибку"""
    return abs((true_value - approx_value) / true_value) * 100
