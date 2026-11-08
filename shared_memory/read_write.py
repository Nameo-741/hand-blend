# import mediapipe as mp
# import cv2
# import json
# import time

# # Initialize MediaPipe Hands
# mp_hands = mp.solutions.hands
# hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)
# mp_drawing = mp.solutions.drawing_utils

# # File to store landmarks
# OUTPUT_FILE = "landmarks.json"

# # Open webcam
# cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# try:
#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break

#         # Flip and convert frame to RGB
#         frame = cv2.flip(frame, 1)
#         frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

#         # Process the frame with MediaPipe Hands
#         results = hands.process(frame_rgb)

#         # Prepare to save landmarks to file
#         landmark_data = {}
#         if results.multi_hand_landmarks:
#             for hand_index, hand_landmarks in enumerate(results.multi_hand_landmarks):
#                 landmarks = {}
#                 for landmark_id, landmark in enumerate(hand_landmarks.landmark):
#                     # Get the landmark name using the enumeration
#                     landmark_name = mp_hands.HandLandmark(landmark_id).name
#                     landmarks[landmark_name] = {
#                         "x": landmark.x,
#                         "y": landmark.y,
#                         "z": landmark.z,
#                     }
#                 landmark_data[f"hand_{hand_index}"] = landmarks

#                 # Draw the landmarks on the frame
#                 mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

#         # Save landmarks to file
#             with open(OUTPUT_FILE, "w") as file:
#                 json.dump(landmarks, file, indent=4)  # Indented for better readability

#         # Display the frame with landmarks
#         cv2.imshow("MediaPipe Hands", frame)

#         # Exit on pressing 'q'
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#         # # Adjust update frequency to avoid high CPU usage
#         # time.sleep(0.05)

# finally:
#     # Release resources
#     cap.release()
#     cv2.destroyAllWindows()
#     hands.close()



import mediapipe as mp
import cv2
import json

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# File to store landmarks
OUTPUT_FILE = "landmarks.json"

# Open webcam
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# List to store all landmark data for every frame
all_landmark_data = []

try:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Flip and convert frame to RGB
        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame with MediaPipe Hands
        results = hands.process(frame_rgb)

        # Prepare landmark data for the current frame
        landmark_data = {}
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                for landmark_id, landmark in enumerate(hand_landmarks.landmark):
                    # Get the landmark name using the enumeration
                    landmark_name = mp_hands.HandLandmark(landmark_id).name
                    landmark_data[landmark_name] = {
                        "x": landmark.x,
                        "y": landmark.y,
                        "z": landmark.z,
                    }

                # Draw the landmarks on the frame
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Append the landmark data for the current iteration to the list
        all_landmark_data.append(landmark_data)

        # Save to file after every iteration
        with open(OUTPUT_FILE, "w") as file:
            json.dump(all_landmark_data, file, indent=4)  # Indented for better readability

        # Display the frame with landmarks
        cv2.imshow("MediaPipe Hands", frame)

        # Exit on pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    # Release resources
    cap.release()
    cv2.destroyAllWindows()
    hands.close()
