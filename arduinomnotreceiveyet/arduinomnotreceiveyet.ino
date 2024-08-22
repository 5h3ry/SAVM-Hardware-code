#include <Stepper.h>

// Number of steps per output rotation
const int stepsPerRevolution = 200;

// Initialize steppers
Stepper stepper1(stepsPerRevolution, 3, 5, 4, 2);
Stepper stepper2(stepsPerRevolution, 7, 9, 8, 6);
Stepper stepper3(stepsPerRevolution, 11, 13, 12, 10);


// Variables to set the number of rotations for each motor
int M1_rotation = 0;
int M2_rotation = 0;
int M3_rotation = 0;

void setup() {
  // Set the speed at 60 rpm for all motors
  stepper1.setSpeed(60);
  stepper2.setSpeed(60);
  stepper3.setSpeed(60);

  // Initialize the serial port
  Serial.begin(115200);

}

void loop() {
  // Check if serial data is available
  if (Serial.available() > 0) {
    // Read the incoming data
    String receivedData = Serial.readStringUntil('\n');

    if (receivedData.indexOf("1708809490064") != -1) {
      int colonIndex = receivedData.indexOf(":");
      if (colonIndex != -1) {
        M1_rotation = receivedData.substring(colonIndex + 1).toInt();
        Serial.print("M1 Rotation: ");
        Serial.println(M1_rotation);
        int steps1 = M1_rotation * stepsPerRevolution;
        
      
        
        stepper1.step(steps1);
        
        // Disable stepper1 after the movement
        delay(1000);
      }
    }

    if (receivedData.indexOf("1708809509998") != -1) {
      int colonIndex = receivedData.indexOf(":");
      if (colonIndex != -1) {
        M2_rotation = receivedData.substring(colonIndex + 1).toInt();
        Serial.print("M2 Rotation: ");
        Serial.println(M2_rotation);

        int steps2 = M2_rotation * stepsPerRevolution;

     
        stepper2.step(steps2);
        
        // Disable stepper2 after the movement
        delay(1000);
      }
    }

    if (receivedData.indexOf("1715846229125") != -1) {
      int colonIndex = receivedData.indexOf(":");
      if (colonIndex != -1) {
        M3_rotation = receivedData.substring(colonIndex + 1).toInt();
        Serial.print("M3 Rotation: ");
        Serial.println(M3_rotation);
        int steps3 = M3_rotation * stepsPerRevolution;

       
        
        stepper3.step(steps3);
        
        // Disable stepper3 after the movement
        delay(1000);
      }
    }
  }
}
