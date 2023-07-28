#include <Servo.h>
#include <stdlib.h>
String inputString = "";
Servo pan, tilt;
bool stringComplete = false;  // whether the string is complete

void setup() {
  // initialize serial:
  Serial.begin(9600);
  // reserve 200 bytes for the inputString:
  inputString.reserve(20);
  pan.attach(12);
tilt.attach(13);
pan.write(90); delay(40);
tilt.write(90); delay(40);
}

void loop() {
  // print the string when a newline arrives:
  if (stringComplete) {
    //Serial.println(inputString);
    if(inputString.substring(0,3) == "pan")
    {
     int pan_val = atoi(inputString.substring(3).c_str());
     Serial.print("pan_val = "); Serial.println(pan_val);
     pan.write(pan_val);
    }
    if(inputString.substring(0,4) == "tilt")
    {
     int tilt_val = atoi(inputString.substring(4).c_str());
     Serial.print("tilt_val = "); Serial.println(tilt_val);
     tilt.write(tilt_val);
    }
    // clear the string:
    inputString = "";
    stringComplete = false;
  }
}

/*
  SerialEvent occurs whenever a new data comes in the hardware serial RX. This
  routine is run between each time loop() runs, so using delay inside loop can
  delay response. Multiple bytes of data may be available.
*/
void serialEvent() {
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read();
    // add it to the inputString:
    inputString += inChar;
    // if the incoming character is a newline, set a flag so the main loop can
    // do something about it:
    if (inChar == '\n') {
      stringComplete = true;
    }
  }
}
