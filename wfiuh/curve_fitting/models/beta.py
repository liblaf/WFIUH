import dataclasses

import numpy as np
import numpy.typing as npt
import scipy.special

from .typed import Model


@dataclasses.dataclass(kw_only=True)
class Beta(Model):
    bounds: tuple[npt.ArrayLike, npt.ArrayLike] = dataclasses.field(
        default=([1, 0], np.inf)
    )

    @staticmethod
    def cdf(t: float | np.ndarray, a: float, b: float) -> float | np.ndarray:
        return scipy.special.betainc(a, b, t)

    @staticmethod
    def pdf(t: float | np.ndarray, a: float, b: float) -> float | np.ndarray:
        u = t ** (a - 1) * (1 - t) ** (b - 1) / scipy.special.beta(a, b)
        if isinstance(u, np.ndarray):
            u[~np.isnan(u)] = 0
        else:
            u = 0 if np.isnan(u) else u
        return u

    def prepare(self, x: np.ndarray, y: np.ndarray) -> None:
        self.sigma = np.ones_like(x)
        self.sigma[[0, -1]] = 0.01
