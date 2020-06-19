String callbackArg;

class CommandHandler {
  public:
    bool newCommand = false; // check if we found a command that has to be processed
    bool execCommand = false;
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
      if (!execCommand) return;
      executeCommand(list, callbacks); // then execute the command
    }

    /**
     * @brief Function that parses the command and arg
     * @detailed Function that parses the command and arg
     * @param list[CH_CSIZE] String Array of strings with a size of CH_CSIZE (defined at start of script). These are the available commands
     */
    void parseCommand(String list[CH_CSIZE]) {
      execCommand = true;
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
      if (!foundMatch) {
        execCommand = false;
        return errorHandler(list, command);
      }
      cmd = command;

      int index = newInpString.indexOf(' ');
      if (index == -1) {
        arg = "";
        return true;
      }
      index++; // add one to get rid of the space
      if (index > newInpString.length()) {
        arg = "";
        return true;
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
//
// // doc further down
// void setLvlCallback(String arg);
// // doc further down
// void getLvlCallback(String arg);
//
// CommandHandler command; // init Command object
// short int level = 0; // short is 16 bit (2 bytes) on every Arduino
// String commands[CH_CSIZE] = {"setBatteryPercentage", "getBatteryPercentage"};
// int callbacks[CH_CSIZE] = {&setLvlCallback, &getLvlCallback};
