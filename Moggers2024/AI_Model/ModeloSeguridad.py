import json
import cv2
from ultralytics import YOLO

# Load a pre-trained YOLO model
model = YOLO("ModelSecurity.pt")

# Define the webcam source (adjust port if needed)
webcam_source = 0

# Capture video frames from webcam
cap = cv2.VideoCapture(webcam_source)

# List of possible objects that may appear
possible_objects = ['Hardhat', 'NO-Hardhat', 'Mask', 'NO-Mask', 'Safety Vest', 'NO-Safety Vest', 'Person', 'Safety Cone', 'machinery', 'vehicle']

# To store the final results per frame
detection_summary = []

# Loop to continuously capture frames from webcam and make predictions
try:
    while True:
        # Capture the frame from the webcam
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame")
            break

        # Perform YOLO prediction on the captured frame
        results = model.predict(source=frame, show=True)

        # Process each result from the YOLO predictions
        for frame_id, result in enumerate(results):
            frame_data = {'frame': frame_id, 'detections': {}}

            # Get the classes detected in the current frame
            detections = result.names  # result.names contains class names like 'Person', 'Hardhat', etc.
            classes = result.boxes.cls  # result.boxes.cls contains the class IDs detected
            counts = {}

            # Count occurrences of each object
            for class_id in classes:
                class_name = detections[int(class_id)]
                if class_name in possible_objects:
                    if class_name not in counts:
                        counts[class_name] = 0
                    counts[class_name] += 1

            # Add counts to frame data
            frame_data['detections'] = counts

            # Append frame data to detection summary
            detection_summary.append(frame_data)

        # Check if the user pressed the 'q' key to exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    # Release the video capture resource and close any open OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

    # Convert the detection summary to JSON format
    json_output = json.dumps(detection_summary, indent=4)

    # Save the JSON output to a file
    with open('detection_summary.json', 'w') as json_file:
        json_file.write(json_output)

    # Optionally, print the JSON output to the console
    print(json_output)
