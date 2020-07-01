#include "Constants.h"
#include "math.h"
#include "EEPROMAnything.h"
#include "SerialControl.h"

// doubles because more precision. Downside is that on some arduinos its 4 bytes and on some its 8 bytes
static double a = 1;
static double b = 1;
static double c = 1;

static double x = 0;
static double y = 0;

static int analogIN = 0;
static int prevAnalogIN = 0;

static int analogOUT = 0;
static int prevAnalogOUT = 0;

static int dOffset = sizeof(a); // this should return the size of a in bytes. We use this to make sure we are storing and reading the correct length from the eeprom
                                // https://www.arduino.cc/reference/en/language/variables/data-types/double/
static bool doDecimalWarn = true;
static bool doVerboseOutput = false;
// forward declaration of functions
double XtoDouble(int* in);
double calcY(double* x);
int YtoAnalog(double* y);

void setA();
void setB();
void setC();
void getABC();
void printY();
void decPrecWarn();
void toggleDecimalWarn();
void toggleVerboseOutput();
void info();
void command_help();

CommandHandler command; // init Command object
short int level = 0; // short is 16 bit (2 bytes) on every Arduino
String commands[CH_CSIZE] = {"setA", "setB", "setC", "getABC", "printY", "toggleVerboseOutput", "toggleDecimalWarn", "info", "help"};
int callbacks[CH_CSIZE] = {&setA, &setB, &setC, &getABC, &printY, &toggleVerboseOutput, &toggleDecimalWarn, &info, &command_help};


void setup() { @FranchuFranchu That one I know about, I'm mainly talking about staff machines not servers
  EEPROM_readAnything(EEPROM_START, a);
  EEPROM_readAnything(EEPROM_START + dOffset, b);
  EEPROM_readAnything(EEPROM_START + 2 * dOffset, c);

  // https://stackoverflow.com/a/570694
  // check for nan, if i != i, i is NaN
  if (a != a) a = 0;
  if (b != b) b = 0;
  if (c != c) c = 0;

  pinMode(O_PIN, OUTPUT); // set pinmode of O_PIN to output
  pinMode(I_PIN, INPUT);  // set pinmode of I_PIN to input
  // initialize serial communications at 9600 bps:
  Serial.begin(9600);
  Serial.println("Arduino Active");
}

void loop() {
  if (command.checkCommand()) { // check for a new command on the serial connection
    command.commandHandler(commands, callbacks);
  }
  // read input
  analogIN = analogRead(I_PIN);
  if (analogIN == prevAnalogIN) return; // if the current analog input is equal to the previous analog input we do not need to do the calculations again
  prevAnalogIN = analogIN;
  // change the input to an x value that can be used to calculate the output
  x = XtoDouble(&analogIN);
  // calc the output
  y = calcY(&x);
  // write the y value casted to an int in the rage of ANALOG_IN_MAX abd ANALOG_IN_MIN
  analogWrite(O_PIN, YtoAnalog(&y));
  if (!doVerboseOutput) return; // check if we want verbose output
  Serial.print("in = ");
  Serial.print(analogIN);
  Serial.print("\nx = ");
  Serial.print(x,             SERIAL_DECIMAL_PRECISION);
  Serial.print("\ny = ");
  Serial.print(y,             SERIAL_DECIMAL_PRECISION);
  Serial.print("\nout = ");
  Serial.print(YtoAnalog(&y));
  Serial.println("\n");
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
 * calculates y based on x and global variables a, b and c
 * @param  x value used to base y on
 * @return   y
 */
double calcY(double* x) {
  // ax^2+bx+c
  return a * square(*x) + b * *x + c;
}

/**
 * converts y to a value that can be used in combination with analogWrite
 * @param  y  ANALOG_OUT_MIN <= y <= ANALOG_OUT_MAX
 * @return   value compatible with analogWrite
 */
int YtoAnalog(double* y) {
  return constrain( // return x if a < x < b. else if a > x, return a else if x > b return b
    255 - (ANALOG_OUT_MAX / (V_MAX/ *y)), // since the mosfet we use is inverted (HIGH = closed, LOW = open) we invert the signal in software
    ANALOG_OUT_MIN,
    ANALOG_OUT_MAX
  );
}

/**
 * update A in memory and on EEPROM
 */
void setA() {
  a = callbackArg.toDouble();
  EEPROM_writeAnything(EEPROM_START, a);

  decPrecWarn();
  Serial.print("\tA = ");
  Serial.print(a, SERIAL_DECIMAL_PRECISION);
  Serial.print("\n");
}

/**
 * update B in memory and on EEPROM
 */
void setB() {
  b = callbackArg.toDouble();
  EEPROM_writeAnything(EEPROM_START + dOffset, b);

  decPrecWarn();
  Serial.print("\tB = ");
  Serial.print(b, SERIAL_DECIMAL_PRECISION);
  Serial.print("\n");
}

/**
 * update C in memory and on EEPROM
 */
void setC() {
  c = callbackArg.toDouble();
  EEPROM_writeAnything(EEPROM_START + 2 * dOffset, c);

  decPrecWarn();
  Serial.print("\tC = ");
  Serial.print(c, SERIAL_DECIMAL_PRECISION);
  Serial.print("\n");
}

/**
 * print A, B and C and formula on Serial connection
 */
void getABC() {
  decPrecWarn();
  Serial.print("\tA = ");
  Serial.print(a,   SERIAL_DECIMAL_PRECISION);
  Serial.print("\n\tB = ");
  Serial.print(b,   SERIAL_DECIMAL_PRECISION);
  Serial.print("\n\tC = ");
  Serial.print(c,   SERIAL_DECIMAL_PRECISION);

  Serial.print("\n\ty = ");
  Serial.print(a,   SERIAL_DECIMAL_PRECISION);
  Serial.print("x^2+");
  Serial.print(b,   SERIAL_DECIMAL_PRECISION);
  Serial.print("x+");
  Serial.println(c, SERIAL_DECIMAL_PRECISION);
}

/**
* calculate Y with the ABC values currently in memory
*/
void printY() {
  double arg = callbackArg.toDouble();
  double y_out = calcY(&arg);

  decPrecWarn();
  Serial.println(y_out, SERIAL_DECIMAL_PRECISION);
}

/**
* print a warning about always printing a set amount of decimal precision
*/
void decPrecWarn() {
  if (!doDecimalWarn) return;
  Serial.println(
    "The serial output is limited to " + String(SERIAL_DECIMAL_PRECISION) + " decimals.\n\
    Internally the numbers are stored as <long> and have 4 to 8 bits of precision (depending on board).\n\
    See:\nhttps://www.arduino.cc/reference/en/language/variables/data-types/long/\
    \nhttps://www.arduino.cc/reference/en/language/functions/communication/serial/print/\n\
    \tYou can disable this message with \"toggleDecimalWarn\"\n"
  );
}

/**
 * toggle the decimal inaccuracy warning
 */
void toggleDecimalWarn() {
  doDecimalWarn = !doDecimalWarn;
  Serial.print("Switching decimal warning to ");
  Serial.println(doDecimalWarn ? "shown" : "hidden");
}

/**
 * switch verbose output
 */
void toggleVerboseOutput() {
  doVerboseOutput = !doVerboseOutput;
  Serial.println("Verbose output is set to " + String(doVerboseOutput ? "True" : "False"));
}

/**
 * print info about loaded sketch
 */
void info() {
  Serial.println("This board is running Electric-Fuel-Gauge v" + String(CURRENT_VERSION));
  Serial.println("\tFor source code please refer to https://github.com/Joeri-G/SchilderElectricBrandstofMeter");
}

/**
* List all available commands
*/
void command_help() {
  Serial.println("Available commands are");
  for (size_t i = 0; i < CH_CSIZE; i++)
  Serial.println("\t" + commands[i]);
}
