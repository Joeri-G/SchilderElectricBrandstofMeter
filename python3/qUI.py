import quadraticSolver as qs
# (0;0.83) (50;2.12) (100;3.06) => -0.00007x^2+0.0293x+0.83
print("V1.0. Developed by Joeri Geuzinge")

xvalues = []
yvalues = []
for i in range(1,4):
    if i == 1:
        print("\tx1 = 0")
        xvalues.append("0")
    else:
        xvalues.append(input("\tx%s = " % i))
    yvalues.append(input("\ty%s = " % i))
    print()

func1 = qs.qFunc(xvalues, yvalues)
formula = func1.getFormula()

print("\n\t%s" % formula)
