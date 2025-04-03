# Traffic Light Detection and Geolocation

This repository contains a Python script for detecting traffic lights in street-view images and geolocating them using camera metadata. It utilizes YOLOv9 for object detection and ArcGIS functionalities for spatial analysis.

## Table of Contents

- [Description](#description)
- [Installation](#installation)
- [Usage](#usage)
- [Dependencies](#dependencies)
- [Data Requirements](#data-requirements)
- [Output](#output)
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
