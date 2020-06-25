#include <iostream>
#include <cmath>
#include <bits/stdc++.h>
#include "Constants.h"

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

int main(int argc, char const *argv[]) {
  int analogRead = 0;
  std::cout << "analogRead = ";
  std::cin >> analogRead;

  std::cout << "\nx = " << (double) XtoDouble(&analogRead) << "\n";
  return 0;
}
