#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
import decimal, sys, os
"""
This script creates a quadratic formula (ax^2+bx+c) based on three or more points
It is not 100% accurate as it suffers from floating point inaccuracy.
For example, the points (0, 0.1) (2.5, 1.05) and (5, 2.3) should yield 0.024x^2+0.32x+0.1
but due to the inaccuracies this script will return 0.02399999999999998x^2+0.32000000000000023x+0.1.
I have no idea how class LagrangePoly(object) works, I copied an answer from stackoverflow and modified it until it did what I wanted.
Right now we use a Larange Interpolation algorythm to calculate the Y value of 3 points and from there we calculate A, B and C for the quadratic formula.
After that we give the end user the option to draw a graph form x[0,5] and y[0,5]
"""


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


if __name__ == "__main__":
    PATH = os.path.dirname(os.path.realpath(__file__))

    print(PATH+"/Gauge_Calibrator.py\nJoeri Geuzinge\n")

    # check if --help is supplied
    if "--help" in sys.argv:
        print(
        """Function:
Fit a function to a list of points and return values that can be used to calibrate the fuel gauge

Usage:
Universal:
$ python3 Gauge_Calibrator.py [--no-graph || --draw-graph] [--percentage || --voltage] [-v int] [-p <points>]

OSX / Linux:
$ ./Gauge_Calibrator.py [--no-graph || --draw-graph] [--percentage || --voltage] [-v int] [-p <points>]

Windows only:
$ py Gauge_Calibrator.py [--no-graph || --draw-graph] [--percentage || --voltage] [-v int] [-p <points>]

Arguments:
  --draw-graph    Draw graph (default = ask)
  --no-graph      Don't draw graph (default = ask)

  --percentage    The X coordinate represents a percentage
  --voltage       The X coordinate represents a voltage (Vin)

  -v <voltage>    Voltage that represents a 100% load

  -p <points>     Supply points as argument point = (x,y) || ( x ; y ) or a variation.
                  Whitespaces are not counted and comma and semicolon are interchangeable. Decimal delimiter is period (.)."""
                  )
        exit()

    # check if points have been supplied via the arguments
    if "-p" in sys.argv:
        if len(sys.argv) <= sys.argv.index("-p") or sys.argv[sys.argv.index("-p") + 1][0] == "-":
            raise ValueError("-p must be followed by a string containing the points")

        pointData = splitPoints(sys.argv[sys.argv.index("-p") + 1])
        if (pointData['valid'] != True):
            exit("Could not find formula. Please check your formatting \"(x;y)\" and enter the points from smallest t")
    else:
        pointData = {
            'valid': False
        }
    # keep on asking for points until the input is valid
    while not pointData['valid']:
        print("Please enter 3 or more points from smallest to largest\n\t(x,y) with either a comma or a semicolon to separate x and y. Whitepsaces are optional\n");
        inp = input("points: ")
        pointData = splitPoints(inp)

    # Chec if Vmax has been supplied
    if "-v" in sys.argv and len(sys.argv)-1 > sys.argv.index("-v") and isfloat(sys.argv[sys.argv.index("-v")+1]):
        Vmax = float(sys.argv[sys.argv.index("-v")+1])
    else:
        Vmax = False
    # check if x = Vin or %

    # make sure --percentage and --voltage are not both supplied
    if "--percentage" in sys.argv and "--voltage" in sys.argv:
        raise ValueError("--percentage cannot be used in combination with --voltage")

    if "--percentage" in sys.argv:

        # If Vmax has not been supplied as an argument
        if not Vmax:
            Vmax = input("Vmax (def = 5): ")

            if isfloat(Vmax):
                Vmax = float(Vmax)

            else:
                Vmax = 5

        for i in range(len(pointData['points'])):
            x = pointData['points'][i][0]
            pointData['points'][i][0] = Vmax * (x / 100)

    elif "--voltage" in sys.argv:
        pass


    else:
        xType = input("is x Vin or % (0 - 100)? [Vin/%] ")
        if xType.upper() not in ["VIN", "%"]:
            raise ValueError("X must be Vin or %")

        if xType.upper() == "%":
            # If Vmax has not been supplied as an argument
            if not Vmax:
                Vmax = input("Vmax (def = 5): ")
                if isfloat(Vmax):
                    Vmax = float(Vmax)
                else:
                    Vmax = 5

            for i in range(len(pointData['points'])):
                x = pointData['points'][i][0]
                pointData['points'][i][0] = Vmax * (x / 100)


    ff = Find_Formula(pointData['points'])

    # find quadratic equation
    ff.find()

    pd = ff.pd

    print("f = %sx^2+%sx+%s\n\ta = %s\n\tb = %s \n\tc = %s" % (pd.a, pd.b, pd.c, pd.a, pd.b, pd.c))

    # ask to open graph window only if the --no-graph is not set
    if '--no-graph' not in sys.argv and ('--show-graph' in sys.argv or input("Draw graph? [Y/n]").upper() == "Y"):
        ff.plot()
