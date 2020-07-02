#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np
import decimal, sys

# I have no idea how this does it, but it works
# https://stackoverflow.com/a/58885954
class LagrangePoly(object):

    def __init__(self, X, Y):
        self.n = len(X)
        self.X = np.array(X)
        self.Y = np.array(Y)

    def basis(self, x, j):
        b = [(x - self.X[m]) / (self.X[j] - self.X[m])
             for m in range(self.n) if m != j]
        return np.prod(b, axis=0) * self.Y[j]

    def interpolate(self, x):
        b = [self.basis(x, j) for j in range(self.n)]
        return np.sum(b, axis=0)


class PointData(object):
    def __init__(self, points):
        super(PointData, self).__init__()
        self.points = points

        self.x = []
        self.y = []

        self.a = 0
        self.b = 0
        self.c = 0

        # f(x) = ax^2+bx+c
        self.f = lambda x : self.a * x ** 2 + self.b * x + self.c

        # put the x and y values in two lists
        for p in points:
            if p[0] in self.x:
                raise ValueError("Invalid points list, same x coordinate found twice")
            self.x.append(p[0])
            self.y.append(p[1])



class Find_Formula(object):
    def __init__(self, points):
        super(Find_Formula, self).__init__()
        self.pd = PointData(points)
            # make sure we don't have an x value twice

        self.lp = LagrangePoly(self.pd.x, self.pd.y)

        # return {'a': a, 'b': b, 'c': c}

    def find(self):
        # place y for x = n in variable for readability
        # convert to decimal for extra precision
        f0 = decimal.Decimal(self.lp.interpolate(0))
        f1 = decimal.Decimal(self.lp.interpolate(1))
        f2p5 = decimal.Decimal(self.lp.interpolate(2.5))
        f5 = decimal.Decimal(self.lp.interpolate(5))
        # c = 0a + 0b + c = c
        c = f0
        # a = ((25a + 5b) - (6.25a + 2.25b) * 2) / 12.5 = 12.5a / 12.5 = a
        a = ((f5 - c) - (f2p5 - c) * 2) / decimal.Decimal(12.5)
        # b = ax + bx + c - a - c = bx = 1b = b
        b = f1 - c - a
        # convert to float for compatability
        self.pd.a = float(a)
        self.pd.b = float(b)
        self.pd.c = float(c)

    def plot(self):
        start = -0
        end = 5
        step = 0.01
        xValues = np.arange(start, end + step, step)
        yValuesInterpolated = self.lp.interpolate(xValues)

        yValuesCalculated = []
        for x in xValues:
            yValuesCalculated.append(self.pd.f(x))

        if type(yValuesInterpolated).__name__ != "ndarray":
            yValuesInterpolated = []
            for x in xValues:
                yValuesInterpolated.append(self.lp.interpolate(x))

        plt.plot(xValues, yValuesInterpolated)
        plt.plot(xValues, yValuesCalculated)

        plt.scatter(self.pd.x, self.pd.y, c='k') # rgb(100,100,100)

        plt.xlim(0, 5)
        plt.ylim(0, 5)

        plt.show(block=True)

def splitPoints(inp):
    # valid inputs
    # (x,y) (x; y)(x,y)
    out = {
        'x':        [],
        'y':        [],
        'points':   [],
        'valid':    True
    }
    # remove spaces
    inp = inp.replace(" ", "")
    inp = inp.replace("\t", "")
    inp = inp.replace("\n", "")
    # replace comma with semicolon
    inp = inp.replace(",", ";")
    # make sure the first and last characters are brackets
    if (inp[0] != "(" or inp[-1] != ")"):
        out['valid'] = False
        return out
    # make sure all the characters are in the of the correct type
    for c in inp:
        if (c not in ["(", ")", ".", ";", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]):
            out['valid'] = False
            return out
    # remove the first and last char
    inp = inp[1:-1]
    # split input by )(
    inp = inp.split(")(")
    for point in inp:
        xy = point.split(";")
        if len(xy) != 2:
            out['valid'] = False
            return out

        x = float(xy[0])
        y = float(xy[1])

        out['x'].append(x)
        out['y'].append(y)
        out['points'].append([x, y])

    for i in range(len(out['x'])):
        if i > 0:
            if out['x'][i] <= out['x'][i-1]:
                out['valid'] = False
                return out

    return out

def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False
