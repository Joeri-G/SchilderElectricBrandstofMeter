#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, findLib, os
"""
This script creates a quadratic formula (ax^2+bx+c) based on three or more points
It is not 100% accurate as it suffers from floating point inaccuracy.
For example, the points (0, 0.1) (2.5, 1.05) and (5, 2.3) should yield 0.024x^2+0.32x+0.1
but due to the inaccuracies this script will return 0.02399999999999998x^2+0.32000000000000023x+0.1.
I have no idea how class LagrangePoly(object) works, I copied an answer from stackoverflow and modified it until it did what I wanted.
Right now we use a Larange Interpolation algorythm to calculate the Y value of 3 points and from there we calculate A, B and C for the quadratic formula.
After that we give the end user the option to draw a graph form x[0,5] and y[0,5]
"""

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

        pointData = findLib.splitPoints(sys.argv[sys.argv.index("-p") + 1])
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
        pointData = findLib.splitPoints(inp)

    # Chec if Vmax has been supplied
    if "-v" in sys.argv and len(sys.argv)-1 > sys.argv.index("-v") and findLib.isfloat(sys.argv[sys.argv.index("-v")+1]):
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

            if findLib.isfloat(Vmax):
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
                if findLib.isfloat(Vmax):
                    Vmax = float(Vmax)
                else:
                    Vmax = 5

            for i in range(len(pointData['points'])):
                x = pointData['points'][i][0]
                pointData['points'][i][0] = Vmax * (x / 100)


    ff = findLib.Find_Formula(pointData['points'])

    # find quadratic equation
    ff.find()

    pd = ff.pd

    print("f = %sx^2+%sx+%s\n\ta = %s\n\tb = %s \n\tc = %s" % (pd.a, pd.b, pd.c, pd.a, pd.b, pd.c))

    # ask to open graph window only if the --no-graph is not set
    if '--no-graph' not in sys.argv and ('--show-graph' in sys.argv or input("Draw graph? [Y/n]").upper() == "Y"):
        ff.plot()
