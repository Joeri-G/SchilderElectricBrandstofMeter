#!/usr/bin/env python3
import decimal
import numpy as np

def format_float(num):
    return np.format_float_positional(num, trim='-')

class qFunc(object):
    """Object used to calculate the formula for a cubic equation (ax^2+bx+c). decimals are requried for precision"""

    def __init__(self, xvalues = [0, 100, 50], yvalues = [0, 0, 0]):
        super(qFunc, self).__init__()
        self.checked = False
        # make sure the input is a list/array and is the same length as the x values
        if type(yvalues).__name__ != "list" or type(xvalues).__name__ != "list" or len(yvalues) != len(xvalues) or len(xvalues) != 3:
            print("Argument is not a list or is not long enough")
            return
        self.yvalues = yvalues
        self.xvalues = xvalues
        self.yvalues = yvalues
        # make sure every value is either an integer or a float/real
        for y in self.yvalues:
            if type(y).__name__ not in ["int", "float", "float64", "decimal"]:
                print("Cannot determine function because %s is not an allowed variable type" % type(y).__name__)
                return
        for x in self.xvalues:
            if type(x).__name__ not in ["int", "float", "float64", "decimal"]:
                print("Cannot determine function because %s is not an allowed variable type" % type(x).__name__)
                return
        if self.xvalues[0] != 0:
            print("x[0] has to be equal to 0 (zero)")
            return

        self.checked = True

    def getFormulaObject(self):
        if (self.checked != True):
            print("Cannot determine formule with given input")
            return
        c = self.calcC()
        b = self.calcB(c)
        a = self.calcA(b, c)
        return {
            'a': a,
            'b': b,
            'c': c,
            'formula': "%sx^2+%sx+%s" % (format_float(a), format_float(b), format_float(c))
        }

    def getFormula(self):
        if (self.checked != True):
            print("Cannot determine formule with given input")
            return
        c = self.calcC()
        b = self.calcB(c)
        a = self.calcA(b, c)
        return "%sx^2+%sx+%s" % (format_float(a), format_float(b), format_float(c))

    def calcC(self):
        if (self.checked != True):
            print("Cannot determine formule with given input")
            return
        # function used to calculate C
        # for this we assume x1 = 0
        c = self.yvalues[0]
        return c

    def calcB(self, c = 0):
        if (self.checked != True):
            print("Cannot determine formule with given input")
            return
        # function used to calculate B
        x1 = self.xvalues[1]
        x2 = self.xvalues[2]
        y1 = self.yvalues[1] - c
        y2 = self.yvalues[2] - c

        ratio = x2**2 / x1**2
        # ratio = x2^2 / x1^2
        # a*x1^2 + b*x1 = y1
        # a*x2^2 + b*x2 = y2
        # a*x1^2*(x2^2/x1^2) + bx1(x2^2/x1^2) = y1(x2^2/x1^2)
        # b = ((x2^2/x1^2)*y1 - y2) / x2
        b = (ratio*y1-y2) / x2
        return b

    def calcA(self, b, c):
        if (self.checked != True):
            print("Cannot determine formule with given input")
            return
        # function used to calculate A
        # a*x1^2+b*x1 = y1
        # a*x1^2 = y1-b*x1
        # a = (y1-b*x1)/x1^2
        y1 = self.yvalues[1] - c
        x1 = self.xvalues[1]
        a = (y1-b*x1)/x1**2
        return a
