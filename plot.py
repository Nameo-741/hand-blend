import cv2
import mediapipe as mp
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.7)

# Initialize Live Plot
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')

# Function to update the plot
def update_plot(landmarks, connections):
    ax.clear()

    if landmarks:
        # Extract coordinates
        x, y, z = zip(*landmarks)

        # Plot the landmarks
        ax.scatter(x, y, z, c='r', marker='o', s=20, label="Landmarks")

        # Plot the connections
        for connection in connections:
            start_idx, end_idx = connection
            ax.plot(
                [x[start_idx], x[end_idx]],  # X-coordinates
                [y[start_idx], y[end_idx]],  # Y-coordinates
                [z[start_idx], z[end_idx]],  # Z-coordinates
                'b-', linewidth=2
            )


    # Set labels and limits
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_zlim(-1, 1)
    ax.set_title("Live 3D Hand Landmarks")
    plt.pause(0.001)

# Open webcam
cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Flip frame horizontally and convert to RGB
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process frame
    result = hands.process(rgb_frame)

    # Draw landmarks and extract them
    landmarks = []
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            landmarks = [(lm.x, lm.y, lm.z) for lm in hand_landmarks.landmark]

    # Update 3D plot
    update_plot(landmarks, mp_hands.HAND_CONNECTIONS if landmarks else [])

    # Display webcam feed
    cv2.imshow('Hand Detection', frame)
    if cv2.waitKey(1) & 0xFF == 27:  # Press ESC to exit
        break

cap.release()
cv2.destroyAllWindows()
plt.close()
