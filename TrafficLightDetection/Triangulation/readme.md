# Traffic Light Detection and Geolocation

This repository contains a Python script for detecting traffic lights in street-view images and geolocating them using camera metadata. It utilizes YOLOv9 for object detection and ArcGIS functionalities for spatial analysis.

## Table of Contents

- [Description](#description)
- [Installation](#installation)
- [Usage](#usage)
- [Dependencies](#dependencies)
- [Data Requirements](#data-requirements)
- [Output](#output)
- [Function Explanations](#function-explanations)
- [License](#license)

## Description

The script performs the following tasks:

1.  **Object Detection:** Uses a pretrained YOLOv9 model to detect traffic lights in a set of street-view images.
2.  **Image Processing:** Draws bounding boxes around detected traffic lights and saves the modified images.
3.  **Geolocation:** Calculates the geographic coordinates of the detected traffic lights by intersecting lines of sight from consecutive images, using camera metadata from a CSV file.
4.  **Spatial Data Creation:** Creates a spatial DataFrame with the geolocated traffic light points and exports it as a feature class to an ArcGIS geodatabase.

## Installation

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  **Ensure you have the necessary data:**
    * Street view images in a directory.
    * A CSV file containing camera metadata.
    * A YOLOv9 pretrained model (`yolov9e.pt`).
    * An ArcGIS Geodatabase.

2.  **Modify the script:**
    * Update the `sampleDir` variable to the path of your image directory.
    * Update the `image_meta_data` variable to the path of your camera metadata CSV file.
    * Update the `yolo` variable to the path of your YOLO model.
    * Update the `gdb` variable to the path of your output Geodatabase.

3.  **Run the script:**

    ```bash
    python <script_name>.py
    ```

## Dependencies

* `os`
* `json`
* `cv2` (OpenCV)
* `math`
* `numpy`
* `itertools`
* `pandas`
* `zipfile`
* `pathlib`
* `arcgis` (arcgis.geometry, arcgis.gis)
* `ultralytics` (YOLO)

You can install these dependencies using the `requirements.txt` file provided:

```bash
pip install -r requirements.txt
Example requirements.txt file:

Plaintext

opencv-python
numpy
pandas
arcgis
ultralytics
Data Requirements
Street-view Images: A directory containing street-view images in .tif format.
Camera Metadata CSV: A CSV file containing camera metadata with the following columns:
Name: Image file name (without extension).
SHAPE: Geometry of the camera location (as a JSON string).
CamHeading: Camera heading angle.
HFOV: Horizontal field of view.
VFOV: Vertical field of view.
FarDist: Far distance for line of sight calculation.
OBJECTID: Object ID of the camera location.
YOLOv9 Model: A pretrained YOLOv9 model (yolov9e.pt).
ArcGIS Geodatabase: An existing ArcGIS geodatabase for output.
Output
The script generates the following outputs:

Marked Images: Images with bounding boxes around detected traffic lights, saved in a new directory (traffic_light_marked_<yolo_model_name>).
JSON File: A JSON file (traffic_light_data_sample.json) containing the coordinates of detected traffic lights in each image.
Feature Class: A feature class (exported_traffic_points_<yolo_model_name>) in the specified ArcGIS geodatabase, containing the geolocated traffic light points.
Function Explanations
traffic_light_finder(oriented_image_path):

This function takes the path to an image as input.
It uses the YOLOv9 model to detect objects in the image.
It filters the detected objects for "traffic light" labels.
For each detected traffic light, it extracts the bounding box coordinates and confidence score.
It draws bounding boxes and labels on the image.
It returns a dictionary containing the detection information (coordinates, object label) and the modified image.
If no traffic lights are found, it returns a dictionary indicating such and the original image.
find_intersection(x1, y1, x2, y2, x3, y3, x4, y4):

This function takes the coordinates of two line segments as input.
It calculates the intersection point of the two lines.
It returns the coordinates of the intersection point as a list [px, py].
ccw(A, B, C):

This function determines the orientation of three points (counter-clockwise, clockwise, or collinear).
It is used to determine if two line segments intersect.
It returns a boolean.
intersect(A, B, C, D):

This function determines if two line segments intersect.
It utilizes the ccw function.
It returns a boolean.
dotdict(dict):

This class extends the Python dictionary to allow access to dictionary elements using dot notation (e.g., dict.key instead of dict['key']).
It improves code readability.
process(input_list, threshold=(10, 15)):

This function takes a list of points as input.
It removes redundant points that are too close to each other, based on a specified threshold.
It returns a list of unique points.
This function is used to help cluster and remove duplicate points that are very close to one another.
