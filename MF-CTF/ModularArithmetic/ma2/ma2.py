# # Коэффициенты Безу Пусть a и b - положительные целые числа. Расширенный алгоритм Евклида - эффективный способ
# найти u, v такие целые числа , что a * u + b * v = gcd(a, b) Числа u, v еще называют коэффициенты Безу. Позже,
# когда мы будем взламывать RSA, нам понадобится этот алгоритм для вычисления модульной инверсии публичной
# экспоненты. А пока, используя два взаимно простых числа p = 25513, q = 32921 и расширенный алгоритм Евклида,
# найдите u, v такие целые числа , что p * u + q * v = gcd(p, q) Ответ введите в виде crypto{u,v} Зная, что p,
# q - взаимно простые числа, что можно сказать о gcd(p, q) ?

def bezout_recursive(a, b):
    """A recursive implementation of extended Euclidean algorithm.
    Returns integer x, y and gcd(a, b) for Bezout equation:
        ax + by = gcd(a, b).
    """
    if not b:
        return 1, 0, a
    y, x, g = bezout_recursive(b, a % b)
    return [x, y - (a // b) * x, g]


p = 25513
q = 32921
bezout = bezout_recursive(p, q)
print(bezout)
print("crypto({0},{1})".format(bezout[0], bezout[1]).replace("(", "{").replace(")", "}"))
