
# SafeLine - Worker Safety Monitoring System

## Team: Moggers

Our mission is to improve worker safety in factories through cutting-edge AI and real-time analytics. The **SafeLine** project uses AI-based object detection to monitor workers in factories, ensuring they wear essential safety equipment like hardhats, safety vests, and masks. Data collected is processed via a Flask API and visualized using dashboards to highlight compliance trends and key metrics.

### Key Features

- **Real-time Monitoring**: Uses YOLOv8 for real-time detection of safety equipment in video streams.
- **Flask API for Data Transfer**: The detection data (e.g., employees without hardhats or masks) is transferred from the client (video capture) to a Flask API in JSON format.
- **Analytics and Reporting**: The Flask API stores detection data in a MySQL database, and analytics are performed to determine which employees are not using their required safety equipment and how frequently this occurs.
- **Dashboard Integration**: The project integrates with dashboards like **Grafana** to provide real-time and historical analytics on safety compliance.

### How It Works

1. **YOLOv8 Detection**: 
   - The system utilizes YOLOv8 for detecting objects related to worker safety (e.g., hardhats, masks, vests).
   - Workers are uniquely tracked using **DeepSORT** to maintain consistent identification across video frames.
  
2. **Data Transfer to Flask API**:
   - Once detections are made, the system sends the relevant data (timestamp, worker ID, and missing equipment) to the Flask API via HTTP requests.
   - The data is then parsed and stored in a **MySQL** database hosted on **Google Cloud**.

3. **Database Schema**:
   ```sql
   CREATE TABLE detections (
       id INT AUTO_INCREMENT PRIMARY KEY,
       frame_count INT,
       timestamp DATETIME,
       hardhat INT,
       no_hardhat INT,
       no_mask INT,
       no_safety_vest INT,
       person INT,
       safety_cone INT,
       safety_vest INT,
       machinery INT,
       vehicle INT
   );
   ```

4. **Analytics**:
   - The collected data is used to perform analysis on how many employees are wearing or not wearing safety equipment.
   - Reports are generated to show compliance levels per worker, department, or over specific time periods.
  
5. **Visualization and Dashboard**:
   - Data from MySQL is visualized in **Grafana**, providing two primary metrics:
     - **Safety Compliance Percentage**: The percentage of time employees wear all required equipment.
     - **Risk Percentage**: Time spent without necessary protective equipment.

### Prerequisites

- Python 3.8+
- Flask
- YOLOv8 and DeepSORT
- MySQL
- Grafana for dashboards
- `gspread` for integration with Google Sheets (optional, used for storing summary data)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/SafeLine.git
   cd SafeLine
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up Flask API:
   ```bash
   python serversql.py
   ```

4. Set up YOLOv8 Detection on the client:
   ```bash
   python Combined_Security_Model.py
   ```

5. Ensure MySQL database is running and properly configured:
   ```sql
   CREATE DATABASE safeline;
   USE safeline;
   -- Add table schema as shown in the 'Database Schema' section
   ```

6. Visualize data on Grafana by connecting it to the MySQL database.

### Usage

- **Running the AI Model**:
  Run the detection model on your machine, connected to the camera source:
  ```bash
  python Combined_Security_Model.py
  ```

- **Sending Data to Flask API**:
  The client sends data after every processed frame. You can inspect the Flask API for received data logs.

- **Visualizing Data**:
  Access the Grafana dashboard to visualize key metrics on worker safety and compliance.

### Future Improvements

- **Enhanced Object Detection**: Integrate additional safety equipment detection (e.g., gloves, goggles).
- **Worker Identification**: Use facial recognition or RFID tags to identify specific employees for personalized reports.
- **Automated Alerts**: Implement real-time alerts when non-compliance exceeds a predefined threshold.
