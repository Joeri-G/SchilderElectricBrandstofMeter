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
        out['points'].append((x, y))
    return out
