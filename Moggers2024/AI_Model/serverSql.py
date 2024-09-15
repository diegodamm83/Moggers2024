from flask import Flask, request, jsonify
import mysql.connector
from datetime import datetime

app = Flask(__name__)

# MySQL database connection setup
db = mysql.connector.connect(
    host='34.174.3.88',     # Replace with your actual Cloud SQL public IP
    user='root',            # Replace with your MySQL username
    password='moggers69',    # Replace with your MySQL password
    database='mogger_safety' # Replace with your MySQL database name
)

cursor = db.cursor()

# Endpoint to process detection data
@app.route('/process_detection', methods=['POST'])
def process_detection():
    try:
        data = request.get_json()  # Get the JSON data from the client

        # Extract frame number and detections
        frame_count = data.get('frame')
        detections = data.get('detections')

        # Define labels of interest
        labels_of_interest = ["Hardhat", "NO-Hardhat", "NO-Mask", "Mask", "NO-Safety Vest", "Person", "Safety Cone", "Safety Vest", "machinery", "vehicle"]

        # Count the occurrences of each detection
        label_count = {label: detections.count(label) for label in labels_of_interest}

        # Generate a timestamp for each detection
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Insert detection counts into the MySQL database
        insert_query = """
        INSERT INTO detections (frame_count, timestamp, hardhat, no_hardhat, no_mask, mask, no_safety_vest, person, safety_cone, safety_vest, machinery, vehicle)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (
            frame_count,
            timestamp,
            label_count["Hardhat"],
            label_count["NO-Hardhat"],
            label_count["NO-Mask"],
            label_count["Mask"],
            label_count["NO-Safety Vest"],
            label_count["Person"],
            label_count["Safety Cone"],
            label_count["Safety Vest"],
            label_count["machinery"],
            label_count["vehicle"]
        ))
        db.commit()

        return jsonify({"status": "success", "message": "Data received and stored in MySQL"}), 200
    except Exception as e:
        # In case of error, return a detailed message
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
