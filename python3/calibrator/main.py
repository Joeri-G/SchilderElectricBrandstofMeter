#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import quadraticSolver, LarangeInterpolation, splitpoints, _thread

# (0;0.83) (50;2.12) (100;3.06)
# -0.00007x^2+0.0293x+0.83

pointData = {
    'valid': False
}

while pointData['valid'] != True:
    print("Please enter 3 or more points\n\t(x,y) with either a comma or a semicolon to separate x and y. Whitepsaces are optional");
    inp = input("points: ")
    pointData = splitpoints.splitPoints(inp)

lp = LarangeInterpolation.LagrangePoly(pointData['x'], pointData['y'])
# create new qFunc object
qF = quadraticSolver.qFunc([0, 50, 100], [
    lp.interpolate(0),
    lp.interpolate(50),
    lp.interpolate(100)
])
# solve
formulaData = qF.getFormulaObject()

# print the data
print("\n\ta = %s\n\tb = %s\n\tc = %s\n\tf(x) = %s" % (
    quadraticSolver.format_float(formulaData['a']),
    quadraticSolver.format_float(formulaData['b']),
    quadraticSolver.format_float(formulaData['c']),
    formulaData['formula']
))

# ask to open graph window
if input("Draw graph? [Y/n]").upper() == "Y":
    xx = np.arange(-50, 150)
    plt.plot(xx, lp.interpolate(xx))
    plt.show(block=False)

input("Press enter to exit the program")
