#include <Servo.h>

Servo diverter;
const uint8_t SERVO_PIN = 9;

// Placeholder positions: calibrate against the real mechanism.
const uint8_t RED_POS = 35;
const uint8_t GREEN_POS = 90;
const uint8_t BLUE_POS = 145;
const uint8_t NEUTRAL_POS = 90;

void setup() {
  Serial.begin(115200);
  diverter.attach(SERVO_PIN);
  diverter.write(NEUTRAL_POS);
}

void applyCommand(char c) {
  switch (c) {
    case 'R': diverter.write(RED_POS); break;
    case 'G': diverter.write(GREEN_POS); break;
    case 'B': diverter.write(BLUE_POS); break;
    case 'N': diverter.write(NEUTRAL_POS); break;
  }
}

void loop() {
  while (Serial.available()) {
    char c = Serial.read();
    applyCommand(c);
  }
}
