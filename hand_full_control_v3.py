import cv2
import mediapipe as mp
import json
import socket

# Initialize MediaPipe hand tracking
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Socket setup
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
blender_address = ('127.0.0.1', 5009)

# Set up webcam capture
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Define the names of the hand landmarks based on MediaPipe's index
landmark_names = {
    0: "WRIST",
    1: "THUMB_CMC", 2: "THUMB_MCP", 3: "THUMB_IP", 4: "THUMB_TIP",
    5: "INDEX_FINGER_MCP", 6: "INDEX_FINGER_PIP", 7: "INDEX_FINGER_DIP", 8: "INDEX_FINGER_TIP",
    9: "MIDDLE_FINGER_MCP", 10: "MIDDLE_FINGER_PIP", 11: "MIDDLE_FINGER_DIP", 12: "MIDDLE_FINGER_TIP",
    13: "RING_FINGER_MCP", 14: "RING_FINGER_PIP", 15: "RING_FINGER_DIP", 16: "RING_FINGER_TIP",
    17: "PINKY_MCP", 18: "PINKY_PIP", 19: "PINKY_DIP", 20: "PINKY_TIP"
}

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Process frame
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        all_hands_data = []  # List to store data for all detected hands
        for hand_landmarks in result.multi_hand_landmarks:
            # Extract bone positions
            mp.solutions.drawing_utils.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            hand_data = {}
            for i, landmark in enumerate(hand_landmarks.landmark):
                # Convert normalized coordinates to screen coordinates
                landmark_name = landmark_names.get(i, f"LANDMARK_{i}")
                hand_data[landmark_name] = {
                    "x": landmark.x,
                    "y": landmark.y,
                    "z": landmark.z
                }
            all_hands_data.append(hand_data)

        # Send data as JSON
        try:
            sock.sendto(json.dumps(all_hands_data).encode(), blender_address)
        except Exception as e:
            print(f"Error sending data: {e}")

    # Display the frame
    cv2.imshow('Hand Tracking', frame)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC key pressed
        # Send stop signal to Blender
        try:
            stop_message = "stop"
            sock.sendto(stop_message.encode(), blender_address)
            print("Sending stop signal...")
        except Exception as e:
            print(f"Error sending stop signal: {e}")
        break

cap.release()
cv2.destroyAllWindows()
sock.close()
