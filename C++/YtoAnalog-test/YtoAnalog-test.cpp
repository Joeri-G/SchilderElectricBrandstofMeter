#include "Constants.h"
#include <iostream>

double constrain(double x, double lower, double upper) {
    return std::min(upper, std::max(x, lower));
}

/**
 * converts y to a value that can be used in combination with analogWrite
 * @param  y  ANALOG_OUT_MIN <= y <= ANALOG_OUT_MAX
 * @return   value compatible with analogWrite
 */
int YtoAnalog(double* y) {
  return constrain( // return x if a < x < b. else if a > x, return a else if x > b return b
    (ANALOG_OUT_MAX / (V_MAX/ *y)), // since the mosfet we use is inverted (HIGH = closed, LOW = open) we invert the signal in software
    ANALOG_OUT_MIN,
    ANALOG_OUT_MAX
  );
}

int main(int argc, char const *argv[]) {
  double y = 0;
  std::cout << "y = ";
  std::cin >> y;

  std::cout << "\nanalogWrite = " << (double) YtoAnalog(&y) << "\n";
  return 0;
}
