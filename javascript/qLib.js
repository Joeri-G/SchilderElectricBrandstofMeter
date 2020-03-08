/*
  qLib.js v1.0
  https://github.com/Joeri-G/brandstof-ijker/blob/master/LICENSE | AGPL 3.0
 */
class qFunc {
  constructor(xvalues = ["0", "100", "50"], yvalues = ["0", "0", "0"]) {
    this.checked = false
    // check if input are arrays
    if (!Array.isArray(xvalues) || !Array.isArray(yvalues)) {
      console.error("xvalues and yvalues must be arrays")
      return
    }
    // make sure both inputs are 3 long
    if (xvalues.length !== 3 || yvalues.length !== 3) {
      console.error("xvalues and yvalues must have a length of 3")
      return
    }
    // make sure the inputs are strings, this way they can be converted to Decimals
    let x, y
    for (var i = 0; i < 3; i++) {
      x = xvalues[i]
      y = yvalues[i]
      if (typeof x !== "string" || typeof y !== "string") {
        console.error("One or more items in xvalues or yvalues are not strings")
        return
      }
      xvalues[i] = new Decimal(x)
      yvalues[i] = new Decimal(y)
    }
    // make sure x[0] is equal to zero in order to calculate c
    if (!xvalues[0].equals(0)) {
      console.error("x[0] has to be equal to 0 (zero)")
      return
    }
    this.xvalues = xvalues
    this.yvalues = yvalues
    this.checked = true
  }

  getFormula() {
    if (!this.checked) {
      console.error("Cannot determine formula with given input")
      return
    }
    let c = this.calcC().toPrecision()
    let b = this.calcB(c).toPrecision()
    let a = this.calcA(b, c).toPrecision()
    return a+"x^2+"+b+"x+"+c
  }

  calcC() {
    if (!this.checked) {
      console.error("Cannot determine formula with given input")
      return
    }
    // to calculate C we must assume x1 = 0
    // ax^2+bx+c = y => a0^2 + b0 + c = y => c = y
    let c = this.yvalues[0]
    return c
  }

  calcB(c) {
    if (!this.checked) {
      console.error("Cannot determine formula with given input")
      return
    }
    c = Decimal(c)
    let x1 = this.xvalues[1]
    let x2 = this.xvalues[2]
    let y1 = this.yvalues[1].minus(c)
    let y2 = this.yvalues[2].minus(c)

    let ratio = x2.pow(2).div(x1.pow(2))
    // ratio = x2^2 / x1^2
    // a*x1^2 + b*x1 = y1
    // a*x2^2 + b*x2 = y2
    // a*x1^2*(x2^2/x1^2) + bx1(x2^2/x1^2) = y1(x2^2/x1^2)
    // b = ((x2^2/x1^2)*y1 - y2) / x2

    let b = (ratio.times(y1).minus(y2)).div(x2)

    return b
  }

  calcA(b, c) {
    if (!this.checked) {
      console.error("Cannot determine formula with given input")
      return
    }
    c = Decimal(c)
    b = Decimal(b)
    // function used to calculate A
    // a*x1^2+b*x1 = y1
    // a*x1^2 = y1-b*x1
    // a = (y1-b*x1)/x1^2
    let y1 = this.yvalues[1].minus(c)
    let x1 = this.xvalues[1]
    let a = y1.div(x1.pow(2)).minus(b.times(x1))
    return a
  }
}
