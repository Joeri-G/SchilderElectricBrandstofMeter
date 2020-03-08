#!/usr/bin/env python3
# script intended to solve linear functions where only x and y are known
# ax+b


class linFunc(object):
    """Object used to determine the formula of a linear function (ax+b)"""

    def __init__(self, xvalues = [0, 100],  yvalues = [0, 0]):
        super(linFunc, self).__init__()
        self.checked = False
        # make sure the input is a list/array and is the same length as the x values
        if type(yvalues).__name__ != "list" or type(xvalues).__name__ != "list" or len(yvalues) != len(xvalues):
            print("Argument is not a list or is not long enough")
            return
        self.yvalues = yvalues
        self.xvalues = xvalues
        # make sure every value is either an integer or a float/real
        for y in self.yvalues:
            if type(y).__name__ not in ["int", "long", "float"]:
                print("Cannot determine function because %s is not an allowed variable type" % type(y).__name__)
                return
        for x in self.xvalues:
            if type(x).__name__ not in ["int", "long", "float"]:
                print("Cannot determine function because %s is not an allowed variable type" % type(x).__name__)
                return
        self.checked = True

    def getFormula(self):
        if (self.checked != True):
            print("Cannot calculate formula with given input")
            return
        self.A = self.calcA()
        self.B = self.calcB()

        return "y = %sx+%s" % (self.A, self.B)


    def calcA(self):
        if (self.checked != True):
            print("Cannot calculate A with given input")
            return 0
        # function used to calculate the angle (A) of the formula
        # A = Delta y / Delta x = ( y2 - y1 ) / ( x2 - x1 )
        x1 = self.xvalues[-1]
        x2 = self.xvalues[0]
        y1 = self.yvalues[-1]
        y2 = self.yvalues[0]

        return (y2-y1)/(x2-x1)

    def calcB(self):
        if (self.checked != True):
            print("Cannot calculate B with given input")
            return 0
        # function used to calculate the elevation (B) of the formula
        # B = y - ax
        y = self.yvalues[0]
        x = self.xvalues[0]
        a = self.calcA()

        return y - a*x

x1 = float(input("x1 = "))
y1 = float(input("y1 = "))
x2 = float(input("x2 = "))
y2 = float(input("y2 = "))

func1 = linFunc([x1, x2], [y1, y2])
formula = func1.getFormula()

print(formula)
