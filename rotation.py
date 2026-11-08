import socket
import mediapipe as mp
import cv2
import json
import math

# Initialize socket
HOST = "127.0.0.1"
PORT = 65432
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print("Waiting for Blender to connect...")

conn, addr = server_socket.accept()
print(f"Connected to Blender: {addr}")

# Initialize MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    # Draw landmarks on the image if detected
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp.solutions.drawing_utils.draw_landmarks(
                frame, hand_landmarks, mp_hands.HAND_CONNECTIONS
            )
            point_4 = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            point_8 = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            point_12 = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]

            # Midpoint of 8th and 12th points
            midpoint_x = (point_8.x + point_12.x) / 2
            midpoint_y = (point_8.y + point_12.y) / 2

            # Calculate the angle with respect to the x-axis
            dx = midpoint_x - point_4.x
            dy = midpoint_y - point_4.y
            angle = math.atan2(dy, dx)  # Radians
            angle_degrees = math.degrees(angle)  # Convert to degrees

            # Prepare data for sending
            wrist = results.multi_hand_landmarks[0].landmark[mp_hands.HandLandmark.WRIST]
            data = {'x': wrist.x, 'y': wrist.y, 'z': wrist.z}
            conn.sendall(json.dumps(data).encode('utf-8'))

    # Show the video feed
    cv2.imshow("Hand Tracking", frame)

    # Break on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
conn.close()
server_socket.close()
cv2.destroyAllWindows()
