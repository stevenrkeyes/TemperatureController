# Author: Steven Keyes
# 23 Jan 2012
# module for calculating a linear regression

# here's an implementation of a least squares regression using numpy
# following the suggestions here:
# http://docs.scipy.org/doc/numpy/reference/generated/numpy.linalg.lstsq.html#numpy.linalg.lstsq
import numpy as np

def forecast(points, x):
    Xs = np.array([p[0] for p in points])
    Ys = np.array([p[1] for p in points])
    A = np.vstack([Xs, np.ones(len(Xs))]).T
    m, c = np.linalg.lstsq(A, Ys)[0]
    return m*x+c

# but we could also implement a least squares regression with simpler constructs
