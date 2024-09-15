import cv2
from ultralytics import YOLO
import requests
import json

# YOLO model setup
model = YOLO("ModelSecurity.pt")  # Load the YOLO model locally
webcam_source = 0  # Use your appropriate webcam source

# Backend server URL
url = 'http://<SERVER_IP>:5000/process_detection'  # Replace <SERVER_IP> with your server's IP address

# Capture video frames from the webcam
cap = cv2.VideoCapture(webcam_source)

frame_skip = 10  # Process every nth frame
frame_count = 0  # Frame counter

# Loop to capture and process each frame
while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read from the webcam.")
        break

    frame_count += 1

    # Process every nth frame
    if frame_count % frame_skip == 0:
        # Predict on the current frame
        results = model.predict(source=frame, show=True)

        # Prepare JSON data with detection results
        detections = []
        for result in results:
            for box in result.boxes:
                cls_id = int(box.cls[0])
                label = model.names[cls_id]
                detections.append(label)

        # Create a JSON payload with the detection results
        data = {'frame': frame_count, 'detections': detections}

        # Send the detection results to the backend server
        try:
            response = requests.post(url, json=data)
            print(f"Frame {frame_count}: {detections}")
            print(f"Server response: {response.status_code}, {response.text}")
        except Exception as e:
            print(f"Error sending data to server: {e}")

    # Show the live video feed
    cv2.imshow('Webcam Feed', frame)

    # Break if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture when done
cap.release()
cv2.destroyAllWindows()
