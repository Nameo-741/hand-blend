import mediapipe as mp
import cv2
import socket
import json

# MediaPipe Hands initialization
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)

# Bone-to-landmark mapping
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

# Socket setup
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
blender_address = ('127.0.0.1', 5004)

# Webcam setup
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Check connection to Blender before starting
def check_connection():
    try:
        # Send a test message to Blender to see if the connection works
        test_message = {"status": "ready"}
        sock.sendto(json.dumps(test_message).encode(), blender_address)
        return True
    except Exception as e:
        print(f"Connection error: {e}")
        return False

# Wait for Blender to be ready
print("Waiting for connection to Blender...")
while not check_connection():
    print("Waiting for Blender to start...")
    cv2.waitKey(1000)  # Wait 1 second before retrying

print("Connected to Blender. Sending bone data... Press ESC to exit.")
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Process frame
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            # Draw landmarks on the frame for visualization
            mp.solutions.drawing_utils.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # Prepare the data
            points_data = {}
            for point_name in mp_hands.HandLandmark:
                landmark = hand_landmarks.landmark[point_name]
                points_data[point_name.name] = {
                    "x": landmark.x,
                    "y": landmark.y,
                    "z": landmark.z
                }
            
            # Send the data as JSON to Blender
            sock.sendto(json.dumps(points_data).encode(), blender_address)

    # Display the frame
    cv2.imshow('Hand Tracking', frame)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC key pressed
        # Send stop signal to Blender
        stop_message = "stop"
        sock.sendto(stop_message.encode(), blender_address)
        print("Sending stop signal...")
        break

cap.release()
cv2.destroyAllWindows()
sock.close()



###############################
#####       empty ness   ######
###############################
# import bpy

# # Bone-to-landmark naming for all joints
# bone_to_landmarks = {
#     "thumb_cmc_to_thumb_mcp": ("THUMB_CMC", "THUMB_MCP"),
#     "thumb_mcp_to_thumb_ip": ("THUMB_MCP", "THUMB_IP"),
#     "thumb_ip_to_thumb_tip": ("THUMB_IP", "THUMB_TIP"),
#     "index_mcp_to_index_pip": ("INDEX_FINGER_MCP", "INDEX_FINGER_PIP"),
#     "index_pip_to_index_dip": ("INDEX_FINGER_PIP", "INDEX_FINGER_DIP"),
#     "index_dip_to_index_tip": ("INDEX_FINGER_DIP", "INDEX_FINGER_TIP"),
#     "middle_mcp_to_middle_pip": ("MIDDLE_FINGER_MCP", "MIDDLE_FINGER_PIP"),
#     "middle_pip_to_middle_dip": ("MIDDLE_FINGER_PIP", "MIDDLE_FINGER_DIP"),
#     "middle_dip_to_middle_tip": ("MIDDLE_FINGER_DIP", "MIDDLE_FINGER_TIP"),
#     "ring_mcp_to_ring_pip": ("RING_FINGER_MCP", "RING_FINGER_PIP"),
#     "ring_pip_to_ring_dip": ("RING_FINGER_PIP", "RING_FINGER_DIP"),
#     "ring_dip_to_ring_tip": ("RING_FINGER_DIP", "RING_FINGER_TIP"),
#     "pinky_mcp_to_pinky_pip": ("PINKY_MCP", "PINKY_PIP"),
#     "pinky_pip_to_pinky_dip": ("PINKY_PIP", "PINKY_DIP"),
#     "pinky_dip_to_pinky_tip": ("PINKY_DIP", "PINKY_TIP"),
#     "wrist_to_thumb_cmc": ("WRIST", "THUMB_CMC"),
#     "wrist_to_index_mcp": ("WRIST", "INDEX_FINGER_MCP"),
#     "wrist_to_middle_mcp": ("WRIST", "MIDDLE_FINGER_MCP"),
#     "wrist_to_ring_mcp": ("WRIST", "RING_FINGER_MCP"),
#     "wrist_to_pinky_mcp": ("WRIST", "PINKY_MCP"),
# }

# # Armature name
# ARMATURE_NAME = "Armature"
# armature = bpy.data.objects.get(ARMATURE_NAME)

# if not armature:
#     raise ValueError(f"Armature '{ARMATURE_NAME}' not found. Check your Blender file.")

# # Ensure armature is the active object
# bpy.context.view_layer.objects.active = armature

# # Switch to Edit Mode to access the bones
# bpy.ops.object.mode_set(mode='EDIT')

# # Iterate over all bones and their corresponding landmark names
# for bone_name, (start_point, end_point) in bone_to_landmarks.items():
#     # Get the bone by name
#     bone = armature.data.edit_bones.get(bone_name)
#     if not bone:
#         print(f"Bone '{bone_name}' not found. Skipping...")
#         continue

# #    # Create empty at the bone's head (joint location) and name it after the start_point
# #    empty = bpy.data.objects.new(start_point, None)
# #    bpy.context.collection.objects.link(empty)
# #    empty.empty_display_size = 0.02
# #    empty.empty_display_type = 'SPHERE'
# #    empty.location = armature.matrix_world @ bone.head  # World space location

#     # Create empty at the bone's tail (finger tip location) and name it after the end_point
#     empty_tip = bpy.data.objects.new(end_point, None)
#     bpy.context.collection.objects.link(empty_tip)
#     empty_tip.empty_display_size = 0.02
#     empty_tip.empty_display_type = 'SPHERE'
#     empty_tip.location = armature.matrix_world @ bone.tail  # World space location

# # Switch back to Object Mode
# bpy.ops.object.mode_set(mode='OBJECT')

# print("Empties created at each joint with appropriate names.")

# # Create an empty at the origin (0, 0, 0)
# empty = bpy.data.objects.new("WRIST", None)
# bpy.context.collection.objects.link(empty)

# # Set the empty's display settings
# empty.empty_display_size = 0.02
# empty.empty_display_type = 'SPHERE'

# # Set the location of the empty at the origin
# empty.location = (0, 0, 0)

# print("Empty named 'Wrist' created at the origin.")



# #################################
# ######### adding constraints ####
# #################################

# #import bpy

# ## Define bone to target mapping (without the "Target" suffix)
# #bone_to_target = {
# #    "wrist_to_thumb_cmc": "THUMB_CMC",
# #    "wrist_to_index_mcp": "INDEX_FINGER_MCP",
# #    "wrist_to_middle_mcp": "MIDDLE_FINGER_MCP",
# #    "wrist_to_ring_mcp": "RING_FINGER_MCP",
# #    "wrist_to_pinky_mcp": "PINKY_MCP",
# #    "thumb_cmc_to_thumb_mcp": "THUMB_CMC",
# #    "thumb_mcp_to_thumb_ip": "THUMB_MCP",
# #    "thumb_ip_to_thumb_tip": "THUMB_IP",
# #    "index_mcp_to_index_pip": "INDEX_FINGER_MCP",
# #    "index_pip_to_index_dip": "INDEX_FINGER_PIP",
# #    "index_dip_to_index_tip": "INDEX_FINGER_DIP",
# #    "middle_mcp_to_middle_pip": "MIDDLE_FINGER_MCP",
# #    "middle_pip_to_middle_dip": "MIDDLE_FINGER_PIP",
# #    "middle_dip_to_middle_tip": "MIDDLE_FINGER_DIP",
# #    "ring_mcp_to_ring_pip": "RING_FINGER_MCP",
# #    "ring_pip_to_ring_dip": "RING_FINGER_PIP",
# #    "ring_dip_to_ring_tip": "RING_FINGER_DIP",
# #    "pinky_mcp_to_pinky_pip": "PINKY_MCP",
# #    "pinky_pip_to_pinky_dip": "PINKY_PIP",
# #    "pinky_dip_to_pinky_tip": "PINKY_DIP",
# #}



# #############################################
# ########### IK UPDATE #######################
# #############################################
# import bpy

# # Define bone-to-target mapping (use the end point of each bone chain)
# bone_to_target = {
#     "wrist_to_thumb_cmc": "THUMB_CMC",  # Target the end of the thumb CMC joint
#     "wrist_to_index_mcp": "INDEX_FINGER_MCP",  # Target the end of the index MCP joint
#     "wrist_to_middle_mcp": "MIDDLE_FINGER_MCP",  # Target the end of the middle MCP joint
#     "wrist_to_ring_mcp": "RING_FINGER_MCP",  # Target the end of the ring MCP joint
#     "wrist_to_pinky_mcp": "PINKY_MCP",  # Target the end of the pinky MCP joint
#     "thumb_cmc_to_thumb_mcp": "THUMB_MCP",  # Target the end of the thumb MCP joint
#     "thumb_mcp_to_thumb_ip": "THUMB_IP",  # Target the end of the thumb IP joint
#     "thumb_ip_to_thumb_tip": "THUMB_TIP",  # Target the end of the thumb tip joint
#     "index_mcp_to_index_pip": "INDEX_FINGER_PIP",  # Target the end of the index PIP joint
#     "index_pip_to_index_dip": "INDEX_FINGER_DIP",  # Target the end of the index DIP joint
#     "index_dip_to_index_tip": "INDEX_FINGER_TIP",  # Target the end of the index tip joint
#     "middle_mcp_to_middle_pip": "MIDDLE_FINGER_PIP",  # Target the end of the middle PIP joint
#     "middle_pip_to_middle_dip": "MIDDLE_FINGER_DIP",  # Target the end of the middle DIP joint
#     "middle_dip_to_middle_tip": "MIDDLE_FINGER_TIP",  # Target the end of the middle tip joint
#     "ring_mcp_to_ring_pip": "RING_FINGER_PIP",  # Target the end of the ring PIP joint
#     "ring_pip_to_ring_dip": "RING_FINGER_DIP",  # Target the end of the ring DIP joint
#     "ring_dip_to_ring_tip": "RING_FINGER_TIP",  # Target the end of the ring tip joint
#     "pinky_mcp_to_pinky_pip": "PINKY_PIP",  # Target the end of the pinky PIP joint
#     "pinky_pip_to_pinky_dip": "PINKY_DIP",  # Target the end of the pinky DIP joint
#     "pinky_dip_to_pinky_tip": "PINKY_TIP",  # Target the end of the pinky tip joint
# }

# # Armature name
# ARMATURE_NAME = "Armature"
# armature = bpy.data.objects.get(ARMATURE_NAME)

# if not armature:
#     raise ValueError(f"Armature '{ARMATURE_NAME}' not found. Check your Blender file.")

# # Ensure armature is the active object
# bpy.context.view_layer.objects.active = armature

# # Switch to Pose Mode to apply the IK constraints
# bpy.ops.object.mode_set(mode='POSE')

# # Iterate over the bone-to-target mapping to apply IK constraints
# for bone_name, target_name in bone_to_target.items():
#     # Get the bone in the armature
#     pose_bone = armature.pose.bones.get(bone_name)

#     if not pose_bone:
#         print(f"Bone '{bone_name}' not found. Skipping...")
#         continue

#     # Get the target object (empty)
#     target = bpy.data.objects.get(target_name)
#     if not target:
#         print(f"Target empty '{target_name}' not found. Skipping...")
#         continue

#     # Remove existing IK constraints from the bone
#     for constraint in pose_bone.constraints:
#         if constraint.type == 'IK':
#             pose_bone.constraints.remove(constraint)

#     # Add IK constraint to the bone
#     ik_constraint = pose_bone.constraints.new(type='IK')
#     ik_constraint.target = target  # Set the target empty for the IK
#     ik_constraint.subtarget = target.name  # The name of the target object (empty)

#     # Set the chain length to include multiple bones in the chain
# #    ik_constraint.chain_length = 2  # Adjust chain length if necessary

#     # Print confirmation
#     print(f"IK constraint applied to bone '{bone_name}' with target '{target_name}' and .")

# # Switch back to Object Mode
# bpy.ops.object.mode_set(mode='OBJECT')

# print("IK constraints applied to all bones.")

# ###################################################
# #######    IK TESTING #############################
# ###################################################
# import bpy
# import socket
# import json
# from mathutils import Vector

# # Socket setup
# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# sock.bind(('127.0.0.1', 5004))  # Adjust this to match your sender's address and port
# sock.setblocking(False)  # Non-blocking socket

# # IK target naming convention (matches joint names in incoming data)
# ik_targets = {
#     "THUMB_CMC": "THUMB_CMC",
#     "THUMB_MCP": "THUMB_MCP",
#     "THUMB_IP": "THUMB_IP",
#     "THUMB_TIP": "THUMB_TIP",
#     "INDEX_FINGER_MCP": "INDEX_FINGER_MCP",
#     "INDEX_FINGER_PIP": "INDEX_FINGER_PIP",
#     "INDEX_FINGER_DIP": "INDEX_FINGER_DIP",
#     "INDEX_FINGER_TIP": "INDEX_FINGER_TIP",
#     "MIDDLE_FINGER_MCP": "MIDDLE_FINGER_MCP",
#     "MIDDLE_FINGER_PIP": "MIDDLE_FINGER_PIP",
#     "MIDDLE_FINGER_DIP": "MIDDLE_FINGER_DIP",
#     "MIDDLE_FINGER_TIP": "MIDDLE_FINGER_TIP",
#     "RING_FINGER_MCP": "RING_FINGER_MCP",
#     "RING_FINGER_PIP": "RING_FINGER_PIP",
#     "RING_FINGER_DIP": "RING_FINGER_DIP",
#     "RING_FINGER_TIP": "RING_FINGER_TIP",
#     "PINKY_MCP": "PINKY_MCP",
#     "PINKY_PIP": "PINKY_PIP",
#     "PINKY_DIP": "PINKY_DIP",
#     "PINKY_TIP": "PINKY_TIP",
# }

# bone_to_landmarks = {
#     "thumb_cmc_to_thumb_mcp": ("THUMB_CMC", "THUMB_MCP"),
#     "thumb_mcp_to_thumb_ip": ("THUMB_MCP", "THUMB_IP"),
#     "thumb_ip_to_thumb_tip": ("THUMB_IP", "THUMB_TIP"),
#     "index_mcp_to_index_pip": ("INDEX_FINGER_MCP", "INDEX_FINGER_PIP"),
#     "index_pip_to_index_dip": ("INDEX_FINGER_PIP", "INDEX_FINGER_DIP"),
#     "index_dip_to_index_tip": ("INDEX_FINGER_DIP", "INDEX_FINGER_TIP"),
#     "middle_mcp_to_middle_pip": ("MIDDLE_FINGER_MCP", "MIDDLE_FINGER_PIP"),
#     "middle_pip_to_middle_dip": ("MIDDLE_FINGER_PIP", "MIDDLE_FINGER_DIP"),
#     "middle_dip_to_middle_tip": ("MIDDLE_FINGER_DIP", "MIDDLE_FINGER_TIP"),
#     "ring_mcp_to_ring_pip": ("RING_FINGER_MCP", "RING_FINGER_PIP"),
#     "ring_pip_to_ring_dip": ("RING_FINGER_PIP", "RING_FINGER_DIP"),
#     "ring_dip_to_ring_tip": ("RING_FINGER_DIP", "RING_FINGER_TIP"),
#     "pinky_mcp_to_pinky_pip": ("PINKY_MCP", "PINKY_PIP"),
#     "pinky_pip_to_pinky_dip": ("PINKY_PIP", "PINKY_DIP"),
#     "pinky_dip_to_pinky_tip": ("PINKY_DIP", "PINKY_TIP"),
#     "wrist_to_thumb_cmc": ("WRIST", "THUMB_CMC"),
#     "wrist_to_index_mcp": ("WRIST", "INDEX_FINGER_MCP"),
#     "wrist_to_middle_mcp": ("WRIST", "MIDDLE_FINGER_MCP"),
#     "wrist_to_ring_mcp": ("WRIST", "RING_FINGER_MCP"),
#     "wrist_to_pinky_mcp": ("WRIST", "PINKY_MCP"),
# }

# # Reference length landmarks
# REFERENCE_START = "WRIST"
# REFERENCE_END = "MIDDLE_FINGER_MCP"
# REFERENCE_DISTANCE = 0.386  # Reference distance in meters (adjust based on your system)

# # Dictionary to store initial bone lengths
# initial_bone_lengths = {}

# # Store the initial lengths of bones at script start
# def store_initial_bone_lengths():
#     armature = bpy.data.objects.get("Armature")  # Replace 'Armature' with your armature's name
#     if not armature or not armature.pose:
#         print("Armature not found or invalid. Ensure the correct armature name.")
#         stop_script()
#         return

#     bpy.context.view_layer.objects.active = armature
#     bpy.ops.object.mode_set(mode='POSE')

#     for bone_name in bone_to_landmarks.keys():
#         bone = armature.pose.bones.get(bone_name)
#         if bone:
#             initial_bone_lengths[bone_name] = bone.length
#         else:
#             print(f"Bone {bone_name} not found in armature. Skipping...")
#             stop_script()

# # Timer function to update IK targets
# def receive_data():
#     try:
#         data, _ = sock.recvfrom(4096)
#         message = data.decode('utf-8')

#         # Stop script if "stop" signal received
#         if message.strip().lower() == "stop":
#             print("Received stop signal. Exiting...")
#             stop_script()
#             return None

#         # Parse JSON data
#         coordinates = json.loads(message)

#         # Ensure reference landmarks exist
#         if REFERENCE_START not in coordinates or REFERENCE_END not in coordinates:
#             print(f"Reference landmarks {REFERENCE_START} or {REFERENCE_END} missing. Skipping frame.")
#             stop_script()
#             return

#         # Calculate scale normalization factor
#         start_pos = Vector((
#             coordinates[REFERENCE_START]["x"],
#             coordinates[REFERENCE_START]["z"],
#             -coordinates[REFERENCE_START]["y"]
#         ))
#         end_pos = Vector((
#             coordinates[REFERENCE_END]["x"],
#             coordinates[REFERENCE_END]["z"],
#             -coordinates[REFERENCE_END]["y"]
#         ))
#         current_distance = (end_pos - start_pos).length
#         scale_factor = REFERENCE_DISTANCE / current_distance if current_distance > 0 else 1.0

#         # Update IK targets
#         for landmark, target_name in ik_targets.items():
#             if landmark not in coordinates:
#                 print(f"Landmark {landmark} missing in data. Skipping...")
#                 stop_script()
#                 continue

#             target_empty = bpy.data.objects.get(target_name)
#             if not target_empty:
#                 print(f"Target empty {target_name} not found in the scene. Skipping...")
#                 stop_script()
#                 continue

#             # Normalize position and update the target
#             raw_pos = Vector((
#                 coordinates[landmark]["x"],
#                 coordinates[landmark]["z"],
#                 -coordinates[landmark]["y"]
#             ))
#             normalized_pos = (raw_pos - start_pos) * scale_factor
#             target_empty.location = normalized_pos

#             # Adjust bone length to match initial length
#             bone_length = initial_bone_lengths.get(target_name, None)
#             if bone_length:
#                 armature = bpy.data.objects.get("Armature")  # Replace 'Armature' with your armature name
#                 if armature and armature.pose:
#                     bone = armature.pose.bones.get(target_name)
#                     if bone:
#                         direction = (target_empty.location - bone.head)
#                         bone.tail = bone.head + direction.normalized() * bone_length

#     except BlockingIOError:
#         pass  # No data received, continue
#     except json.JSONDecodeError as e:
#         print(f"Error decoding JSON: {e}")
#     except Exception as e:
#         print(f"Unexpected error: {e}")

#     return 0.1  # Reschedule the function to run again in 0.1 seconds

# # Function to stop the script
# def stop_script():
#     try:
#         bpy.app.timers.unregister(receive_data)
#         sock.close()
#         print("Script stopped.")
#     except ValueError:
#         print("Script already stopped.")

# # Store initial bone lengths
# store_initial_bone_lengths()

# # Register the timer function
# bpy.app.timers.register(receive_data)

# print("Blender script is running and listening for hand tracking data...")
