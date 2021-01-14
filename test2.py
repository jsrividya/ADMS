from scipy.misc import derivative


def f(x):
    return x**3 + x**2

print(derivative(f(2), 2.0))
