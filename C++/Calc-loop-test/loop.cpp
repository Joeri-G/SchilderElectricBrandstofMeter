#include <iostream>
#include <cmath>
#include <bits/stdc++.h>
#include "Constants.h"

// comp functions
double constrain(double x, double lower, double upper);
double square(double base);

// forward declaration of functions
double XtoDouble(int* in);
double calcY(double* x);
int YtoAnalog(double* y);

const static double a = 0;
const static double b = 1;
const static double c = 0.1;

int main(int argc, char const *argv[]) {
  int analogIN = 0;
  int analogOUT = 0;
  double x = 0;
  double y = 0;

  std::cout << "analogIN = ";
  std::cin >> analogIN;

  x = XtoDouble(&analogIN);
  y = calcY(&x);
  analogOUT = YtoAnalog(&y);

  std::cout << "\nX = " << x;
  std::cout << "\nY = " << y;
  std::cout << "\nAnalogOut = " << analogOUT << "\n";

  return 0;
}


double square(double base) {
  return std::exp(base);
}

double constrain(double x, double lower, double upper) {
    return std::min(upper, std::max(x, lower));
}

/**
 * converts input from analogRead to double value between X_MIN and X_MAX
 * @param  in ANALOG_IN_MIN <= in <= ANALOG_IN_MAX
 * @return    return a double that can be used to calculate y
 */
double XtoDouble(int* in) {
  return constrain( // return x if a < x < b. else if a > x, return a else if x > b return b
    V_MAX / (ANALOG_IN_MAX / (double) *in), // typecast to double because somehow it would return an int if I didnt
    ANALOG_IN_MIN,
    ANALOG_IN_MAX
  );
}

/**
 * converts y to a value that can be used in combination with analogWrite
 * @param  y  ANALOG_OUT_MIN <= y <= ANALOG_OUT_MAX
 * @return   value compatible with analogWrite
 */
int YtoAnalog(double* y) {
  return constrain( // return x if a < x < b. else if a > x, return a else if x > b return b
    ANALOG_OUT_MAX - (ANALOG_OUT_MAX / (V_MAX/ *y)), // since the mosfet we use is inverted (HIGH = closed, LOW = open) we invert the signal in software
    ANALOG_OUT_MIN,
    ANALOG_OUT_MAX
  );
}

/**
 * calculates y based on x and global variables a, b and c
 * @param  x value used to base y on
 * @return   y
 */
double calcY(double* x) {
  // ax^2+bx+c
  return a * square(*x) + b * *x + c;
}
