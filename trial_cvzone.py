import cvzone
import cv2
from cvzone.HandTrackingModule import HandDetector
import serial
import time



cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands = 2, detectionCon=0.8 )

try:
    arduino = serial.Serial(port='COM10', baudrate=115200, timeout=0.1)
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
    exit()

def send_command(command):
    """Send command to Arduino."""
    try:
        arduino.write(bytes(command + '\n', 'utf-8'))
        time.sleep(0.05)  # Small delay to ensure data is sent
    except Exception as e:
        print(f"Error sending command: {e}")

while True:
    success, img = cap.read()
    if not success:
        break

    hands, img = detector.findHands(img)
    if hands:
        for hand in hands:
            
            fingers = detector.fingersUp(hand)
            print(fingers)

              # Convert the fingers list to a string with '$' prefix
            fingers_string = '$' + ''.join(str(int(finger)) for finger in fingers)
            
            # Send the string to Arduino
            send_command(fingers_string)

            
           
    cv2.imshow("Image", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()