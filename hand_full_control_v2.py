import mediapipe as mp
import cv2
import socket
import json
import time  # Importing time to add a delay

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)

# Set up socket connection
HOST = '127.0.0.1'  # Localhost
PORT = 65432        # Port to send data on
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
print("Connected to Blender")

# Define the mapping between bone names and corresponding landmarks
bone_to_landmarks = {
    "thumb_cmc_to_thumb_mcp": ("THUMB_CMC", "THUMB_MCP"),
    "thumb_mcp_to_thumb_ip": ("THUMB_MCP", "THUMB_IP"),
    "thumb_ip_to_thumb_tip": ("THUMB_IP", "THUMB_TIP"),
    "index_mcp_to_index_pip": ("INDEX_FINGER_MCP", "INDEX_FINGER_PIP"),
    "index_pip_to_index_dip": ("INDEX_FINGER_PIP", "INDEX_FINGER_DIP"),
    "index_dip_to_index_tip": ("INDEX_FINGER_DIP", "INDEX_FINGER_TIP"),
    "middle_mcp_to_middle_pip": ("MIDDLE_FINGER_MCP", "MIDDLE_FINGER_PIP"),
    "middle_pip_to_middle_dip": ("MIDDLE_FINGER_PIP", "MIDDLE_FINGER_DIP"),
    "middle_dip_to_middle_tip": ("MIDDLE_FINGER_DIP", "MIDDLE_FINGER_TIP"),
    "ring_mcp_to_ring_pip": ("RING_FINGER_MCP", "RING_FINGER_PIP"),
    "ring_pip_to_ring_dip": ("RING_FINGER_PIP", "RING_FINGER_DIP"),
    "ring_dip_to_ring_tip": ("RING_FINGER_DIP", "RING_FINGER_TIP"),
    "pinky_mcp_to_pinky_pip": ("PINKY_MCP", "PINKY_PIP"),
    "pinky_pip_to_pinky_dip": ("PINKY_PIP", "PINKY_DIP"),
    "pinky_dip_to_pinky_tip": ("PINKY_DIP", "PINKY_TIP"),
    "wrist_to_thumb_cmc": ("WRIST", "THUMB_CMC"),
    "wrist_to_index_mcp": ("WRIST", "INDEX_FINGER_MCP"),
    "wrist_to_middle_mcp": ("WRIST", "MIDDLE_FINGER_MCP"),
    "wrist_to_ring_mcp": ("WRIST", "RING_FINGER_MCP"),
    "wrist_to_pinky_mcp": ("WRIST", "PINKY_MCP"),
}

# Start capturing video
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

try:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture image. Retrying...")
            continue  # Retry capturing if frame is not available

        # Convert frame to RGB for MediaPipe processing
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame with MediaPipe
        results = hands.process(frame_rgb)

        # Prepare data for sending
        hand_landmarks = {}
        if results.multi_hand_landmarks:
            for hand_landmark in results.multi_hand_landmarks:
                # Extract and map the landmarks to bones
                for bone_name, (start_landmark, end_landmark) in bone_to_landmarks.items():
                    start_idx = mp_hands.HandLandmark[start_landmark]
                    end_idx = mp_hands.HandLandmark[end_landmark]

                    # Get the coordinates of the start landmark
                    start_coords = hand_landmark.landmark[start_idx]
                    start_position = {
                        'x': start_coords.x,
                        'y': start_coords.y,
                        'z': start_coords.z
                    }

                    # Send the bone name and the start position
                    hand_landmarks[bone_name] = start_position

                    # Optionally, draw the landmarks on the frame for debugging
                    # Convert the landmark's coordinates to pixel values
                    h, w, _ = frame.shape
                    start_x = int(start_coords.x * w)
                    start_y = int(start_coords.y * h)

                    # Draw a circle at the start of the bone
                    cv2.circle(frame, (start_x, start_y), 5, (0, 255, 0), -1)

        # Send the landmarks as JSON data
        try:
            client_socket.sendall(json.dumps(hand_landmarks).encode('utf-8'))
        except Exception as e:
            print(f"Error sending data: {e}")
            break  # Break the loop if there is an issue with sending data

        # Optional: Display the video with landmarks (for debugging)
        for hand_landmark in results.multi_hand_landmarks or []:
            mp.solutions.drawing_utils.draw_landmarks(frame, hand_landmark, mp_hands.HAND_CONNECTIONS)

        # Show the frame with the drawn landmarks
        cv2.imshow("MediaPipe Hands", frame)

        # Add a small delay to allow data to be sent properly and to reduce CPU usage
        time.sleep(0.1)  # Delay of 0.1 seconds

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break  # Exit if 'q' is pressed

except Exception as e:
    print(f"Error: {e}")

finally:
    # Clean up
    cap.release()
    cv2.destroyAllWindows()
    client_socket.close()
