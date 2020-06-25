#define CH_CSIZE 9  // num of commands and callbacks

#define CURRENT_VERSION "0.1.4"

#define SERIAL_DECIMAL_PRECISION 5 // decimals precision in output

// The L stand for "Long double" This way I dont have to type cast in the functions

#define I_PIN A0  // input pin  must be analog (marked with ~ in schematic)
#define O_PIN 11  // output pin must be analog (marked with ~ in schematic)

#define Y_MIN 0L  // min value of y
#define Y_MAX 5L  // max value of y

#define X_MIN 0L    // min value of x
#define X_MAX 100L  // max value of x

#define ANALOG_OUT_MIN 0L   // min analogWrite out
#define ANALOG_OUT_MAX 255L // max analogWrite out

#define ANALOG_IN_MIN 0L    // min analogRead
#define ANALOG_IN_MAX 1023L // max analogRead

#define V_MAX 5L  // maximum input voltage

#define EEPROM_START 0 // start of part of EEPROM that is used for config
