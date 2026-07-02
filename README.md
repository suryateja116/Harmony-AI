# Harmony AI Monitoring System

Harmony is a real-time AI-powered computer vision system designed to monitor waste disposal behavior through accurate spatial reasoning. Unlike conventional surveillance systems that rely solely on object detection, Harmony combines **YOLOv8**, **Bird's Eye View (BEV) transformation**, and **homography-based distance estimation** to understand interactions between people, litter, and disposal bins in real-world environments.

The system continuously detects relevant objects, transforms the scene into a geometrically consistent top-down representation, estimates real-world distances, and analyzes behavioral patterns using a Finite State Machine (FSM). When improper waste disposal behavior is identified, Harmony provides real-time audio feedback to encourage responsible environmental practices.

---

# Key Features

- Real-time object detection using YOLOv8
- Homography-based Bird's Eye View (BEV) transformation
- Accurate real-world distance estimation
- Human-object interaction analysis
- Finite State Machine (FSM) for behavioral modeling
- Real-time audio feedback system
- CPU-friendly real-time inference
- Live visualization of both camera and BEV views
- Modular and scalable architecture

---

# Motivation

Traditional CCTV systems are passive—they record events but cannot interpret human behavior. Existing AI-based monitoring systems often rely on pixel distances, which suffer from perspective distortion and produce inaccurate spatial measurements.

Harmony addresses this limitation by transforming the camera view into a Bird's Eye View, allowing Euclidean distances to closely represent real-world distances. This significantly improves the reliability of interaction detection and behavioral analysis.

---

# System Architecture

```text
                           Camera
                              │
                              ▼
                     Video Frame Capture
                              │
                              ▼
                   YOLOv8 Object Detection
                              │
                              ▼
              Ground Contact Point Extraction
                              │
                              ▼
               Homography Transformation
                              │
                              ▼
                 Bird's Eye View Generation
                              │
                              ▼
                 Real-World Distance Estimation
                              │
                              ▼
            Finite State Machine (Behavior Analysis)
                              │
                              ▼
             Audio Feedback & Live Visualization
```

---

# Technology Stack

| Category | Technologies |
|----------|--------------|
| Programming Language | Python |
| Computer Vision | OpenCV |
| Object Detection | Ultralytics YOLOv8 |
| Numerical Computing | NumPy |
| Audio System | Pygame |
| Spatial Reasoning | Homography, Bird's Eye View |
| Behavioral Logic | Finite State Machine (FSM) |

---

# Behavioral State Machine

Harmony models human behavior using a Finite State Machine consisting of four states:

| State | Description |
|--------|-------------|
| **IDLE** | No meaningful interaction detected. |
| **OBSERVING** | A person approaches a detected waste object. |
| **NUDGING** | The person remains near the waste object beyond a predefined threshold, triggering an audio reminder. |
| **COMPLIANCE** | Proper waste disposal is detected and the interaction concludes successfully. |

---

# Workflow

1. Capture live video from a fixed surveillance camera.
2. Detect people, waste objects, and disposal bins using YOLOv8.
3. Extract the ground contact point for each detected object.
4. Apply homography transformation to generate a Bird's Eye View.
5. Estimate real-world distances between detected entities.
6. Analyze spatial relationships through a Finite State Machine.
7. Trigger real-time audio feedback when non-compliant behavior is detected.
8. Display both the original camera feed and transformed BEV visualization.

---

# Performance

The Harmony system demonstrates significant improvements over traditional pixel-based distance estimation.

| Metric | Result |
|--------|--------|
| Mean Absolute Error (MAE) | **0.027 m** |
| Root Mean Square Error (RMSE) | **0.028 m** |
| Improvement over Pixel-Based Estimation | **95.2%** |
| Runtime Performance | **~14 FPS (CPU Only)** |

---

# Applications

Harmony can be adapted for a variety of intelligent monitoring scenarios, including:

- Smart campuses
- Educational institutions
- Corporate offices
- Public spaces
- Smart city infrastructure
- Environmental monitoring
- Automated waste management
- Human-object interaction analysis

---

# Future Enhancements

- Multi-camera support
- Automatic camera calibration
- Multi-object tracking
- Outdoor deployment support
- Custom-trained litter detection models
- Analytics dashboard
- Activity recognition using advanced AI models
- Cloud-based monitoring and reporting

---

# Repository Structure

```text
Harmony/
│
├── models/                 # Detection models
├── calibration/            # Homography calibration files
├── audio/                  # Audio prompts
├── utils/                  # Utility modules
├── outputs/                # Generated outputs
├── main.py                 # Main application
├── requirements.txt        # Python dependencies
└── README.md
```

---

# Installation

```bash
git clone https://github.com/<your-username>/Harmony.git

cd Harmony

pip install -r requirements.txt
```

---

# Usage

```bash
python main.py
```

---

# Research Contribution

Harmony demonstrates that integrating deep learning-based object detection with geometric perspective correction substantially improves spatial reasoning in computer vision systems. By replacing conventional pixel-based distance estimation with homography-based Bird's Eye View transformation, the system achieves accurate real-world interaction analysis while maintaining real-time performance on consumer-grade CPU hardware.

---

# Author

**Surya Teja Annam**

B.Tech Computer Science (Artificial Intelligence & Machine Learning)

Semester Abroad Programme (SAP)

INTI International University, Malaysia

---

