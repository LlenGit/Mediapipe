import cv2
import mediapipe as mp
import serial
import time

# Initialize MediaPipe Hand module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Set up serial communication with Arduino
try:
    arduino = serial.Serial(port='COM11', baudrate=115200, timeout=.1)  # Increased baud rate for faster communication
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
    exit()

def send_command(command):
    """Send command to Arduino."""
    try:
        arduino.write(bytes(command + '\n', 'utf-8'))
    except Exception as e:
        print(f"Error sending command: {e}")

def get_angles(landmarks):
    """Calculate angles for the thumb and index finger based on landmark positions."""
    if landmarks:
        thumb_tip = landmarks[4].y
        index_tip = landmarks[8].y
        
        # Adjust the multiplier to increase the angle range
        thumb_angle = int(thumb_tip * 300)  # Adjusted to increase rotation to 270 degrees
        index_angle = int(index_tip * 300)
        
        # Ensure angles are within valid servo range
        thumb_angle = max(0, min(thumb_angle, 270))
        index_angle = max(0, min(index_angle, 270))
        
        return thumb_angle, index_angle
    return None, None

# Initialize webcam
cap = cv2.VideoCapture(0)
previous_thumb_angle, previous_index_angle = None, None

frame_count = 0
frame_skip = 2  # Process every 3rd frame

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame from webcam.")
        break

    frame_count += 1
    if frame_count % frame_skip != 0:
        continue

    # Convert the frame to RGB for MediaPipe processing
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame to get hand landmarks
    result = hands.process(rgb_frame)

    # If hand landmarks are detected, process and send commands to Arduino
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Calculate angles for thumb and index finger
            thumb_angle, index_angle = get_angles(hand_landmarks.landmark)

            if (thumb_angle is not None and index_angle is not None and 
                (thumb_angle != previous_thumb_angle or index_angle != previous_index_angle)):

                # Send commands to Arduino only if angles have changed
                send_command(f'INDEX {index_angle}')
                send_command(f'THUMB {thumb_angle}')

                # Update previous angles
                previous_thumb_angle, previous_index_angle = thumb_angle, index_angle
    else:
        # Send "REST" command if no hand is detected
        send_command('REST')

    # Display the processed frame
    cv2.imshow('Hand Tracking', frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
