// modified from https://playground.arduino.cc/Code/EEPROMWriteAnything/ (https://web.archive.org/web/20190417023723/https://playground.arduino.cc/Code/EEPROMWriteAnything/)
#include <EEPROM.h>
#include <Arduino.h>  // for type definitions

template <class T> int EEPROM_writeAnything(int ee, const T & value) {
  const byte* p = (const byte * )(const void * ) & value;
  size_t i;
  size_t s = sizeof(value);
  for (i = 0; i < s; i++)
    EEPROM.write(ee++, * p++);
  return i;
}

template <class T> int EEPROM_readAnything(int ee, T & value) {
  byte* p = (byte * )(void * ) & value;
  size_t i;
  size_t s = sizeof(value);
  for (i = 0; i < s; i++)
    *p++ = EEPROM.read(ee++);
  return i;
}
