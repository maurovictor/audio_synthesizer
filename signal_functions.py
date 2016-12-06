import numpy as np

def degrau(x):
    y = np.zeros(len(x))
    for i in xrange(0,len(x)):
        if x[i] >= 0:
                y[i] = 1
    return y


def rec(n, a, b):
    y = degrau(n - a)
    z = degrau(n - b)
    rec = y - z
    return rec
