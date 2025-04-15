import cv2
import mediapipe as mp
import pyautogui
import numpy as np

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,  # Allow detection of both hands
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

# Get screen dimensions
screen_width, screen_height = pyautogui.size()

# Initialize webcam
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Smoothing factor for mouse movement
smoothing_factor = 2

# Previous coordinates for smoothing
prev_x, prev_y = 0, 0

# Click and drag state
is_dragging = False
click_threshold = 0.05
frames_to_hold = 5  # Number of frames to hold for drag
hold_counter = 0

while True:
    success, img = cap.read()
    if not success:
        break

    # Flip the image horizontally for a later selfie-view display
    img = cv2.flip(img, 1)
    
    # Convert the BGR image to RGB
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Process the image and detect hands
    results = hands.process(img_rgb)
    
    # Initialize hand states
    right_hand_detected = False
    left_hand_detected = False
    
    if results.multi_hand_landmarks:
        for hand_idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
            # Get hand type (left or right)
            hand_type = results.multi_handedness[hand_idx].classification[0].label
            
            # Draw hand landmarks
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # Get finger coordinates
            index_finger = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            
            # Calculate distance between thumb and index finger
            distance = np.sqrt((index_finger.x - thumb_tip.x)**2 + (index_finger.y - thumb_tip.y)**2)
            
            if hand_type == "Right":
                right_hand_detected = True
                # Convert coordinates to screen coordinates
                x = int(index_finger.x * screen_width)
                y = int(index_finger.y * screen_height)
                
                # Smooth mouse movement
                x = prev_x + (x - prev_x) / smoothing_factor
                y = prev_y + (y - prev_y) / smoothing_factor
                
                # Move mouse cursor
                pyautogui.moveTo(x, y)
                
                # Update previous coordinates
                prev_x, prev_y = x, y
                
                # Display hand type
                cv2.putText(img, "Right Hand: Moving", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            
            elif hand_type == "Left":
                left_hand_detected = True
                # Click and drag logic for left hand
                if distance < click_threshold:
                    if not is_dragging:
                        hold_counter += 1
                        if hold_counter >= frames_to_hold:
                            is_dragging = True
                            pyautogui.mouseDown()
                            cv2.putText(img, "Left Hand: Dragging", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    else:
                        cv2.putText(img, "Left Hand: Dragging", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                else:
                    if is_dragging:
                        pyautogui.mouseUp()
                        is_dragging = False
                    elif hold_counter > 0 and hold_counter < frames_to_hold:
                        pyautogui.click()
                    hold_counter = 0
                    cv2.putText(img, "Left Hand: Ready", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    
    # Display the image
    cv2.imshow("Hand Tracking", img)
    
    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows() 