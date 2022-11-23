import scipy.stats


def normal_gaussian(t, a, b):
    return scipy.stats.norm.pdf(x=t, loc=a, scale=b)


def inverse_gaussian(t, a, b):
    return scipy.stats.invgauss.pdf(x=t, mu=b / a, scale=a)


def polynomial(t, a, b, c):
    return 3 * a * t**2 + 2 * b * t + c
