# Traffic Light Detection from Oriented Imagery

This repository contains a complete pipeline for detecting traffic lights in oriented imagery. It leverages a YOLO-based deep learning model for object detection, and integrates with ArcGIS for spatial analysis and export. The code is organized into several sections, including data preparation, detection, spatial processing, and exporting results.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Dependencies](#dependencies)
- [Installation](#installation)
- [Usage](#usage)
- [Function Explanations](#function-explanations)
  - [traffic_light_finder](#traffic_light_finder)
  - [find_intersection](#find_intersection)
  - [ccw](#ccw)
  - [intersect](#intersect)
  - [dotdict](#dotdict)
  - [process](#process)
- [Data and Output](#data-and-output)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

---

## Overview

The pipeline in this project:
- **Prepares Data:** Downloads or references oriented imagery and associated metadata.
- **Detects Traffic Lights:** Uses a pretrained YOLO model (e.g., `yolov9e.pt`) for object detection. Images are processed to annotate traffic lights with bounding boxes.
- **Processes Spatial Data:** Calculates intersection points between detections in consecutive images and clusters redundant points.
- **Exports Results:** Saves annotated images, writes detection details to a JSON file, and exports a spatial feature class for use in ArcGIS.

---

## Features

- **Object Detection:** YOLO model is used to identify traffic lights.
- **Image Annotation:** Draws bounding boxes and labels traffic lights on images.
- **Spatial Analysis:** Computes intersections from sequential image data to pinpoint traffic light positions.
- **Clustering:** Filters and clusters nearby detections to remove redundancy.
- **GIS Integration:** Creates a spatial DataFrame and exports results as a feature class in a file geodatabase.

---

## Dependencies

Ensure you have the following installed:

- **Python 3.x**
- **OpenCV:** `opencv-python`
- **NumPy**
- **Pandas**
- **ArcGIS API for Python:** `arcgis`
- **Ultralytics YOLO:** `ultralytics`

Standard libraries used include `os`, `json`, `math`, `itertools`, `zipfile`, and `pathlib`.

---

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/traffic-light-detection.git
   cd traffic-light-detection
2. Install the Required Dependencies:

```bash
pip install opencv-python numpy pandas arcgis ultralytics
```
3. Set Up Data:
- Update file paths (e.g., sampleDir, filepath, and image_meta_data) in the script to match your local data locations.
- If using ArcGIS Online sample data, adjust the download settings accordingly.

---

Usage
1. Configure Paths:
   *Modify the file paths in the script to point to your local directories where the imagery and metadata are stored.
3. Run the Script:

```bash
python your_script.py
```
The script will:
- Load the YOLO model and perform detection on each image.
- Annotate and save images with detected traffic lights.
- Write detection results to a JSON file.
- Process spatial data from camera metadata and detected bounding boxes.
- Export a spatial DataFrame as a feature class to a file geodatabase.

---

## Function Explanations
### traffic_light_finder
```python
def traffic_light_finder(oriented_image_path):
    flag = 0
    coordlist = []
    temp_list = {}
    results = model(oriented_image_path, conf=0.65)  # Perform inference

    test_img = cv2.imread(oriented_image_path)

    if not results[0].boxes:  # Check if any object was detected.
        temp_list["object"] = False
    else:
        for result in results:
            boxes = result.boxes
            for box in boxes:
                label_index = int(box.cls[0])
                label = model.names[label_index]
                print(label)
                if label.lower() == "traffic light":
                    flag = 1
                    b = box.xyxy[0].cpu().numpy().astype(int)  # Get box coordinates in (left, top, right, bottom) format
                    confidence = float(box.conf[0])
                    coordlist.append(b.tolist())
                    test_img = cv2.rectangle(test_img, (b[0], b[1]), (b[2], b[3]), (0, 0, 255), 10)
                    textvalue = label + "_" + str(confidence)
                    cv2.putText(test_img, textvalue, (b[0], b[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 2)
        if flag == 1:
            temp_list["object"] = True
            temp_list["coords"] = coordlist
            temp_list["assetname"] = "traffic light"
            
    return temp_list, test_img
```
#### What It Does:
- Inference: Runs the YOLO model on an input image.
- Detection Check: Determines if any objects (specifically traffic lights) are detected.
- Annotation: Draws bounding boxes and labels on detected traffic lights.
- Output: Returns a dictionary with detection details and the annotated image.

---

### find_intersection
```python

def find_intersection(x1, y1, x2, y2, x3, y3, x4, y4):
    px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / (
        (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    )
    py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / (
        (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    )
    return [px, py]
```
#### What It Does:
- Intersection Calculation: Computes the intersection point of two lines defined by their endpoints.
- Return: Provides the (x, y) coordinates of the intersection.

---

### ccw
```python

def ccw(A, B, C):
    return (C.y - A.y) * (B.x - A.x) > (B.y - A.y) * (C.x - A.x)
```
####What It Does:
- Orientation Check: Determines if three points (A, B, C) are arranged in a counterclockwise order.
- Return: A boolean value that is used as a helper for line intersection logic.

---

### intersect
```python

def intersect(A, B, C, D):
    return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)
```
####What It Does:
- Intersection Determination: Uses the ccw function to determine if two line segments (A-B and C-D) intersect.
- Return: A boolean indicating whether the two segments intersect.

---

###dotdict
```python

class dotdict(dict):
    """dot.notation access to dictionary attributes"""

    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
```
#### What It Does:
- Dictionary Extension: Subclasses Python’s built-in dict to allow attribute-style access (e.g., point.x instead of point['x']).
- Usage: Simplifies accessing dictionary elements, particularly when working with point coordinates.

---

### process
```python

def process(input_list, threshold=(10, 15)):
    combos = itertools.combinations(input_list, 2)
    points_to_remove = [
        point2
        for (point1, point2) in combos
        if abs(point1[0] - point2[0]) <= threshold[0]
        and abs(point1[1] - point2[1]) <= threshold[1]
    ]
    points_to_keep = [point for point in input_list if point not in points_to_remove]
    return points_to_keep
```
#### What It Does:
- Clustering: Processes a list of points and removes those that are very close to one another (redundant detections).
- Thresholding: Uses a threshold tuple to decide when two points are considered duplicates.
- Return: A filtered list of unique points.

---

# Data and Output
- Annotated Images:
  Images with detected traffic lights are saved in a designated folder (e.g., traffic_light_marked_yolov9e).
- JSON Detection File:
  Detection details (bounding box coordinates, labels, etc.) are stored in a JSON file.
- Spatial Feature Class:
  A spatial DataFrame is created from the detected points and exported as a feature class to a file geodatabase (e.g., DeepLearning.gdb) for use with ArcGIS Online.

---

# Contributing
Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Submit a pull request detailing your changes.

---

# License
This project is licensed under the MIT License.

---

# Acknowledgments
- Ultralytics YOLO: For providing a robust object detection model.
- ArcGIS API for Python: For enabling spatial data processing and export.
- OpenCV, NumPy, and Pandas: For efficient image and data manipulation.

