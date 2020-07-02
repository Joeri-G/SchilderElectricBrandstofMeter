#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import quadraticSolver as qS
import LarangeInterpolation as lI
import splitpoints as sP
import sys
import os
import inspect

"""
This script creates a quadratic formula (ax^2+bx+c) based on three or more points
It is not 100% accurate as it suffers from floating point inaccuracy.
For example, the points (0;0.83), (50;2.12) and (100;3.06) should yield -0.00007x^2+0.0293x+0.83
but due to the inaccuracies this script will return -0.00007000000000000002x^2+0.029300000000000003x+0.83.

I have no idea how LarangeInterpolation.py works, I copied an answer from stackoverflow and modified it until it did what I wanted.
Right now we use an Larange Interpolation algorythm to calculate the Y value of 3 points and from there we calculate A, B and C for the quadratic formula.

After that we give the end user the option to draw a graph form x = -50 to x = 150
"""

# (0;0.83) (50;2.12) (100;3.06)
# -0.00007x^2+0.0293x+0.83x
# -0.00007000000000000002x^2+0.029300000000000003x+0.83

if __name__ == "__main__":
    scriptdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    # check for --help arg
    if "--help" in sys.argv:
        with open(scriptdir+"/help.txt", "r") as f:
            for line in f.readlines():
                print(line, end="")
        exit()


    # check if points have been supplied via the arguments
    if "-p" in sys.argv:
        if len(sys.argv) <= sys.argv.index("-p") or sys.argv[sys.argv.index("-p") + 1][0] == "-":
            exit("-p must be followed by a string containing the points")

        pointData = sP.splitPoints(sys.argv[sys.argv.index("-p") + 1])
        if (pointData['valid'] != True):
            exit("Could not find formula. Please check your formatting \"(x;y)\" and enter the points from smallest t")
    else:
        pointData = {
            'valid': False
        }
    # keep on asking for points until the input is valid
    while pointData['valid'] != True:
        print("Please enter 3 or more points from smallest to largest\n\t(x,y) with either a comma or a semicolon to separate x and y. Whitepsaces are optional\n");
        inp = input("points: ")
        pointData = sP.splitPoints(inp)

    lp = lI.LagrangePoly(pointData['x'], pointData['y'])
    # create new qFunc object
    qF = qS.qFunc([ 0, 50, 100 ], [
        lp.interpolate(0),      # y for x = 0
        lp.interpolate(50),     # y for x = 50
        lp.interpolate(100)     # y for x = 100
    ])
    # solve
    formulaData = qF.getFormulaObject()

    # print the data
    print("\ta = %s\n\tb = %s\n\tc = %s\n\tf(x) = %s" % (
        qS.format_float(formulaData['a']),
        qS.format_float(formulaData['b']),
        qS.format_float(formulaData['c']),
        formulaData['formula']
    ))

    # ask to open graph window only if the --no-graph is not set
    if '--no-graph' not in sys.argv and (
            '--show-graph' in sys.argv or
            input("Draw graph? [Y/n]").upper() == "Y"
        ):
        xx = np.arange(-50, 150)
        yValues = lp.interpolate(xx)

        if type(yValues).__name__ != "ndarray":
            print(type(yValues).__name__)
            yValues = []
            for x in xx:
                yValues.append(lp.interpolate(xx))

        plt.plot(xx, yValues)
        plt.show(block=True)
