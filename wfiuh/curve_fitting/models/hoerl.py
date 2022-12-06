import numpy as np

from .typed import Model


class Hoerl(Model):
    @staticmethod
    def cdf(t: float | np.ndarray, a: float, b: float, c: float) -> float | np.ndarray:
        return a * b**t * t**c

    @staticmethod
    def pdf(t: float | np.ndarray, a: float, b: float, c: float) -> float | np.ndarray:
        return a * b**t * t ** (c - 1) * (np.log(b) * t + c)
