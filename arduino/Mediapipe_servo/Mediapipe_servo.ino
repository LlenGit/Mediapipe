#include <Servo.h>

Servo indexFinger;  // Servo for the index finger
Servo thumb;        // Servo for the thumb

// Define rest positions for the servos
const int REST_INDEX_ANGLE = 90;  // Adjust as needed
const int REST_THUMB_ANGLE = 90;  // Adjust as needed

void setup() {
    Serial.begin(115200);  // Start serial communication
    indexFinger.attach(9);  // Attach index finger servo to pin 9
    thumb.attach(10);       // Attach thumb servo to pin 10
    // Initialize servos to rest position
    indexFinger.write(REST_INDEX_ANGLE);
    thumb.write(REST_THUMB_ANGLE);
}

void loop() {
    if (Serial.available() > 0) {
        String command = Serial.readStringUntil('\n');  // Read the incoming command
        if (command.startsWith("INDEX")) {
            int angle = command.substring(6).toInt();  // Extract the angle for the index finger
            // Ensure angle is within valid range (0 to 270 degrees, adjust as needed)
            angle = constrain(angle, 0, 270);
            indexFinger.write(angle);  // Move the index finger servo to the specified angle
            Serial.println("Index finger moved to " + String(angle) + " degrees");
        }
        else if (command.startsWith("THUMB")) {
            int angle = command.substring(6).toInt();  // Extract the angle for the thumb
            // Ensure angle is within valid range (0 to 270 degrees, adjust as needed)
            angle = constrain(angle, 0, 270);
            thumb.write(angle);  // Move the thumb servo to the specified angle
            Serial.println("Thumb moved to " + String(angle) + " degrees");
        }
        else if (command.startsWith("REST")) {
            // Move servos to rest position
            indexFinger.write(REST_INDEX_ANGLE);
            thumb.write(REST_THUMB_ANGLE);
            Serial.println("Servos moved to rest position");
        }
    }
}
