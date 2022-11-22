import numpy as np


def normal_gaussian(t, a, b):
    return 1 / (b * np.sqrt(2 * np.pi)) * np.exp(-0.5 * ((t - a) / b) ** 2)


def polynomial(t, a, b, c):
    return 3 * a * t**2 + 2 * b * t + c
