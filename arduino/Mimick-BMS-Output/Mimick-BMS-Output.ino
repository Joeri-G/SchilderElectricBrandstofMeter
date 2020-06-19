/*
This script will mimick the PWM output of the BMS.
Adjusting the signal can be done through serial commands
*/

#include "EEPROMAnything.h" // https://playground.arduino.cc/Code/EEPROMWriteAnything/
#define OUTPIN 9   // output pin
#define CH_CSIZE 2  // num of commands and callbacks
#define EEPROM_SIZE 1024
#define EEPROM_START_ADDR 0

String callbackArg;

class CommandHandler {
  public:
    bool newCommand = false; // check if we found a command that has to be processed
    String newInpString;
    String cmd;
    String arg; // Since dynamic memory allocation is a pain on micro controllers I'm not doing it.
    void (*callbackCommandFunction)(void);
    /**
     * @brief Function used to check for new command
     * @detailed Function used to check for new command over a Serial connection and return a boolean
     * @return Bool that indicates wether or not a new command has been received
     */
    bool checkCommand() { // function that check for a new command over Serial and return a boolean accordingly
      String in = Serial.readString();
      if (in.length() > 0 && in != "\r\n" && in != "\n") {
        newCommand = true;
        newInpString = in;
        return true;
      }
      return false;
    }

    /**
     * @brief Function called to parse and execute new command
     * @detailed Function called to parse and execute new command
     * @param list[CH_CSIZE] String Array of strings with a size of CH_CSIZE (defined at start of script). These are the available commands
     * @param callbacks[CH_CSIZE] int Array of pointers to callback functions. Array is the same size as list
     */
    void commandHandler(String list[CH_CSIZE], int callbacks[CH_CSIZE]) { // function that handles the digestion and execution of this new command
      if (!newCommand) {return;} // if we don't have a new command stop execution
      newCommand = false; // set newCommand to false so that we won't do the same thing twice
      parseCommand(list); // parse the command first
      executeCommand(list, callbacks); // then execute the command
    }

    /**
     * @brief Function that parses the command and arg
     * @detailed Function that parses the command and arg
     * @param list[CH_CSIZE] String Array of strings with a size of CH_CSIZE (defined at start of script). These are the available commands
     */
    void parseCommand(String list[CH_CSIZE]) {
      // extract command from command string
      // command stops at first space
      int cmdStop = newInpString.indexOf(' ');
      if (cmdStop < 0) cmdStop = newInpString.length()  ;
      // make sure we cut off the \r\n
      newInpString.replace("\n", "");
      newInpString.replace("\r", "");
      String command = newInpString.substring(0, cmdStop);


      bool foundMatch = false;

      // make sure the command actually exists
      for (size_t i = 0; i < CH_CSIZE; i++) {
        if (list[i] == command) {
          foundMatch = true;
          break;
        }
      }

      // if we did not find a match send the user an error
      if (!foundMatch) return errorHandler(list, command);
      cmd = command;

      int index = newInpString.indexOf(' ');
      if (index == -1) {
        arg = "";
        return;
      }
      index++; // add one to get rid of the space
      if (index > newInpString.length()) {
        arg = "";
        return;
      }
      arg = newInpString.substring(index); // arg are everything after the command
    }

    /**
     * @brief Function that executes the command with arg
     * @detailed Function that executes the command with arg
     * @param list[CH_CSIZE] String Array of strings with a size of CH_CSIZE (defined at start of script). These are the available commands
     * @param callbacks[CH_CSIZE] int Array of pointers to callback functions. Array is the same size as list
     */
    void executeCommand(String list[CH_CSIZE], int callbacks[CH_CSIZE]) {
      for (size_t i = 0; i < CH_CSIZE; i++) {
        if (cmd == list[i]) {
          // execute the callback function
          callbackCommandFunction = callbacks[i];
          callbackArg = arg;
          callbackCommandFunction();
          return;
        }
      }
    }

    /**
     * @brief Function that handles errors
     * @detailed Function that returns an error message and a list of available commands
     * @param list[CH_CSIZE] String list of available commands
     * @param command String Invalid command
     */
    void errorHandler(String list[CH_CSIZE], String command) {
      Serial.println("Could not execute " + command);
      // list available commands
      Serial.println("Available command are: ");
      for (size_t i  = 0; i < CH_CSIZE; i++) {
        Serial.println("\t" + list[i]);
      }
    }

    /**
     * @brief Set command
     * @detailed The function sets a new command as if it was received over Serial
     * @param command String command with arguments that has to be set
     * @param list[CH_CSIZE] String Array of strings with a size of CH_CSIZE (defined at start of script). These are the available commands
     * @param callbacks[CH_CSIZE] int Array of pointers to callback functions. Array is the same size as list
     */
    void setCommand(String command, String list[CH_CSIZE], int callbacks[CH_CSIZE]) {
      newCommand = true;
      newInpString = command;
      commandHandler(list, callbacks);
    }
};

// doc further down
void setLvlCallback(String arg);
// doc further down
void getLvlCallback(String arg);

CommandHandler command; // init Command object
short int level = 0; // short is 16 bit (2 bytes) on every Arduino
String commands[CH_CSIZE] = {"setBatteryPercentage", "getBatteryPercentage"};
int callbacks[CH_CSIZE] = {&setLvlCallback, &getLvlCallback};

void setup() {
  // initialize serial communications at 9600 bps:
  Serial.begin(9600);

  Serial.println("Arduino Active");

  pinMode(OUTPIN, OUTPUT);

  // read the last stored value from the EEPROM
  EEPROM_readAnything(EEPROM_START_ADDR, level);
  if (level < 0 || level > 255) {
    level = 0;
    EEPROM_writeAnything(EEPROM_START_ADDR, level);
  }
  Serial.println("Current percentage is " + String(level * 100 / 255)) + "%";
}

void loop() {
  if (command.checkCommand()) { // check for a new command on the serial connection
    command.commandHandler(commands, callbacks);
  }
  analogWrite(OUTPIN, level);
}


/**
 * @brief Function that updates level
 * @detailed Callback that updates the global level variable. The input is expected to be between 0 and 100 and the level is set to and adjusted int between 0 and 255
 * @param __ignore String just ignore this, the program breaks if I don't have this
 */
void setLvlCallback(String __ignore) {
  // For some reason I have to give it an argument of type String because if I don't it won't compile.
  // I have no idea why this happens, please help
  int inpLvl = callbackArg.toInt();
  if (inpLvl > 100 || inpLvl < 0) {
    Serial.println("Malformed paramater. Must be integer between 0 and 100. Was " + String(inpLvl));
    return;
  }

  level = inpLvl * 255 / 100;
  EEPROM_writeAnything(EEPROM_START_ADDR, level); // update level store in EEPROM
  Serial.println("Lvl set to " + String(callbackArg));
}

/**
 * @brief Function that sends the current level as an int between 0 and 100 over Serial
 * @detailed Function that sends the current level as an int between 0 and 100 over Serial, use -m as a callbackArg to only make it send the level
 */
void getLvlCallback(String __ignore) {
  if (callbackArg == "-m") { // if the minimal flag has been passed
    Serial.print(String(level * 100 / 255));
    return;
  }
  Serial.println("Currently outputting a battery percentage of " + String(level * 100 / 255) + "%");
}
