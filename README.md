---

## Smart Attendance System

The **Smart Attendance System** is a real-time facial recognition-based application designed for educational institutions and organizations to automate the process of attendance tracking. By leveraging computer vision, the system identifies individuals from a camera feed and records their attendance in a CSV file.

### Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [File Structure](#file-structure)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

### Features

- **Real-Time Face Recognition**: Detects and recognizes faces using a live camera feed.
- **Automated Attendance Logging**: Records attendance data (name and timestamp) in a CSV file.
- **Session Management**: Supports starting and stopping attendance sessions.
- **Configurable Settings**: Easily configure paths for known faces and attendance logs.
- **User-Friendly Interface**: Simple GUI built with Tkinter for ease of use.
- **Multi-Camera Support**: Option to select from multiple connected cameras.
- **Security**: Basic user authentication to restrict access.
- **Error Handling**: Graceful handling of exceptions and errors during runtime.

---

### Prerequisites

Before running the Smart Attendance System, ensure you have the following installed:

- **Python 3.x**
- **pip** (Python package manager)

### Installation

1. **Clone the Repository**:

    ```bash
    git clone https://github.com/your-username/smart-attendance-system.git
    cd smart-attendance-system
    ```

2. **Install the Required Packages**:

    Use the following command to install all necessary Python packages:

    ```bash
    pip install -r requirements.txt
    ```

3. **Set Up Known Faces**:

    - Create a directory named `known_faces` in the project root.
    - Add images of known individuals into this directory. Ensure that the file name of each image corresponds to the person’s name (e.g., `john_doe.jpg`).

4. **Configuration**:

    Modify `config.ini` to set paths for the known faces directory and the attendance CSV file. If not provided, default paths will be used.

---

### Configuration

The application uses a `config.ini` file to manage configuration settings. Below is an example configuration:

```ini
[Paths]
KNOWN_FACES_DIR = known_faces
ATTENDANCE_CSV_PATH = attendance.csv

[Camera]
CAMERA_INDEX = 0  # Change to 1, 2, etc., if using a different camera
```

- **`KNOWN_FACES_DIR`**: Directory where known faces are stored.
- **`ATTENDANCE_CSV_PATH`**: Path to the CSV file where attendance will be recorded.
- **`CAMERA_INDEX`**: Index of the camera to be used. Default is `0`.

---

### Usage

1. **Start the Application**:

    Run the Python script to launch the GUI:

    ```bash
    python attendance_system.py
    ```

2. **Using the GUI**:

    - **Start Camera**: Click "Start Camera" to begin face detection and recognition.
    - **Stop Camera**: Click "Stop Camera" to end the session.
    - **Attendance Log**: The right panel shows a log of recorded attendance.

3. **Attendance Log**:

    Attendance is automatically saved in the specified CSV file (`attendance.csv` by default). Each entry includes the name of the recognized individual and the timestamp of attendance.

---

### File Structure

The project structure is organized as follows:

```
smart-attendance-system/
│
├── attendance_system.py        # Main application script
├── README.md                   # Project documentation
├── requirements.txt            # Python dependencies
├── config.ini                  # Configuration file
├── LICENSE                     # License information
├── .gitignore                  # Files to be ignored by Git
├── attendance.csv              # CSV file for attendance logs
└── known_faces/                # Directory for storing known face images
    ├── john_doe.jpg
    └── jane_doe.jpg
```

---

### Troubleshooting

Here are some common issues and solutions:

- **Camera Not Working**:
    - Ensure that your camera is connected properly.
    - Check the `CAMERA_INDEX` in the `config.ini` file and adjust it as necessary.

- **Face Not Recognized**:
    - Ensure the image in the `known_faces` directory is clear and well-lit.
    - Try adding more images of the person in different lighting or angles.

- **Application Freezes**:
    - This might be due to a heavy processing load. Ensure your system meets the requirements and try lowering the camera resolution.

- **CSV File Not Generated**:
    - Ensure that you have write permissions to the directory where the CSV file is being saved.

---

### Contributing

Contributions are welcome! If you have suggestions for improvements or new features, feel free to open an issue or submit a pull request.

1. Fork the repository.
2. Create a new branch: `git checkout -b my-feature-branch`
3. Make your changes and commit them: `git commit -m 'Add my feature'`
4. Push to the branch: `git push origin my-feature-branch`
5. Open a Pull Request.

---

### License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---
