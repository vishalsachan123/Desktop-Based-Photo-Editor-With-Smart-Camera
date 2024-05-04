import os
import cv2
import mediapipe as mp
import time
from datetime import datetime
import random
def myCam():
    # Load pre-trained face cascade classifier
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    #pictures_path = r'D:\Desktop Based Photo Editor\Smart Camera'  
    pictures_path = r'D:\Desktop Based Photo Editor10-dec-23\Smart Camera'

    # Initialize MediaPipe Hands
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands()
    
    # List of possible texts
    texts = ["Intelligent 80%..", "Intelligent 70%..", "Intelligent 50%..", "Intelligent 100%.."]
    
    # Start camera
    cap = cv2.VideoCapture(0)
    
    # Variables for timer and hand gesture detection
    timer_started = False
    start_time = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
    
        # Convert the image to RGB and process it for hand detection
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(image)
    
        # Convert frame to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
        # Detect faces in the grayscale image
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
        # Display the selected text above all detected faces and save an image with text
        frame_with_text = frame.copy()
        for (x, y, w, h) in faces:
            selected_text = random.choice(texts)
            cv2.putText(frame_with_text, selected_text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
            cv2.rectangle(frame_with_text, (x, y), (x + w, y + h), (255, 0, 0), 2)  # Draw a rectangle around the detected face
    
        if results.multi_hand_landmarks:
            # Assuming hand is detected, check for palm gesture
            # Customize this part based on specific hand gesture detection
            # For example, if a palm is detected, start the timer
            timer_started = True
            start_time = time.time()
    
        if timer_started:
            current_time = time.time()
            elapsed_time = current_time - start_time
    
            # Check if 2 seconds have passed after detecting the palm
            if elapsed_time >= 1.0:
                # Save the image with the text
                #print("Image with text captured!")
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                image_name1 = f"SC_With{timestamp}.jpg"
                cv2.imwrite(os.path.join(pictures_path, image_name1), frame_with_text)
    
                # Save the image without the text
                image_name2 = f"SC_Without{timestamp}.jpg"
                cv2.imwrite(os.path.join(pictures_path, image_name2), frame)
                #print("Image without text captured!")
                break
    
        cv2.imshow('Camera', frame_with_text)  # Display the image with text for visual reference
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
