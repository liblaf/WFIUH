import numpy as np

from ..typed import Model


class DoubleTriangular(Model):
    @staticmethod
    def forward(t: float | np.ndarray, a: float, b: float) -> float | np.ndarray:
        def kernel(t: float) -> float:
            if 0 <= t and t <= b * a:
                return 2 * t / a / (a * b)
            elif b * a <= t and t <= a:
                return 2 * (1 - t / a) / (a * (1 - b))
            else:
                return 0  # nan

        if isinstance(t, np.ndarray):
            return np.array(list(map(kernel, t)))
        else:
            return kernel(t)

    def prepare(self, x: np.ndarray, y: np.ndarray) -> None:
        self.p0 = [x.max() + 10, 0.5]
        self.bounds = ([x.max(), 0], [np.inf, 1])