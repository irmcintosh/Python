# Distance and Location Estimation Using Camera and Bearings

This Python project calculates the distance from a camera to an object using computer vision techniques and estimates the new latitude and longitude of the object based on the known camera coordinates, calculated distance, and bearing (direction). The project can be used for real-world applications where geographical location of an object needs to be calculated from images.

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Example Output](#example-output)
- [Bearings](#bearings)
- [Contributing](#contributing)
- [License](#license)

## Project Overview

The primary goal of this project is to:
1. Compute the distance from the camera to an object in an image using the object’s known width and the pixel width in the image.
2. Calculate the new geographic coordinates (latitude and longitude) of the object based on the camera’s location, distance to the object, and bearing (direction).

### Features:
- **Distance Calculation**: Uses focal length and pixel measurements to calculate the distance to the object.
- **Geographical Location**: Calculates new latitude and longitude coordinates using spherical trigonometry based on the camera's position and bearing.
- **Bearing Adjustment**: Allows the user to input custom bearings (e.g., North, East, South, West).

## Installation

### Prerequisites
Ensure you have Python installed on your machine. You'll need the following Python libraries:
- `math` (standard Python library)
- `numpy` (for handling numerical operations)
- `opencv-python` (for computer vision tasks)

You can install the necessary dependencies using `pip`:

```bash
pip install numpy opencv-python
```

### Clone the Repository
To get started with this project, clone the repository to your local machine:

```bash
git clone https://github.com/your-username/distance-location-estimation.git
```

Navigate to the project directory:

```bash
cd distance-location-estimation
```

## Usage

To run the project, create a Python script or Jupyter notebook and use the provided functions.

### Steps:
1. **Pre-calculate the Focal Length**: Using a known object with a known distance from the camera, calculate the focal length.
2. **Calculate the Distance to the Object**: Using the pixel width of the object in the image and the focal length, compute the distance.
3. **Calculate New Latitude and Longitude**: Given the distance, bearing, and camera’s current location, compute the new geographic coordinates.

### Code Example:
Here is an example of how you might use the functions in the script:

```python
import math

# Define known parameters
known_distance = 22.2504  # meters
known_width = 0.762       # meters
pixel_width = 0.047496855  # example pixel width of the object in the image

# Camera's latitude and longitude
camera_lat = 33.5782292
camera_lon = -82.1907745

# Example bearing (in degrees): 45° for Northeast
bearing = 45  

# Calculate the focal length based on known data
focal_length = preFocalLength(pixel_width, known_distance, known_width)

# Calculate the distance to the object
distance = distance_to_camera(known_width, focal_length, pixel_width)

# Calculate the new latitude and longitude
new_lat, new_lon = calculate_new_lat_lon(camera_lat, camera_lon, distance, bearing)

# Output the results
print(f"New Latitude: {new_lat}, New Longitude: {new_lon}")
print(f"Distance: {distance} meters, Focal Length: {focal_length} units")
```

## Example Output

Given the following inputs:
- Known distance: 22.2504 meters
- Known object width: 0.762 meters
- Pixel width of the object: 0.047496855 units
- Camera latitude: 33.5782292
- Camera longitude: -82.1907745
- Bearing: 45° (Northeast)

You may get an output like:

```
New Latitude: 33.5783, New Longitude: -82.19065
Distance: 22.25 meters, Focal Length: 138.94 units
```

## Bearings

Bearings define the direction from the camera to the object. Here are some common bearing values:
- **North (0°)**: Directly in front of the camera (aligned with the Earth's meridian).
- **East (90°)**: To the right of the camera.
- **South (180°)**: Directly behind the camera.
- **West (270°)**: To the left of the camera.
- **Northeast (45°)**, **Southeast (135°)**, **Southwest (225°)**, **Northwest (315°)** are intermediate directions.

You can modify the bearing in the script to represent the direction of the object relative to the camera.

## Contributing

We welcome contributions to improve this project! If you'd like to contribute, please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Submit a pull request.

### TODOs:
- Implement additional features such as angle calculation from image data.
- Improve real-time image processing for better performance.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```

### Instructions for Use:
- Make sure to replace `https://github.com/your-username/distance-location-estimation.git` with your actual GitHub repository link.
- Update the `TODOs` section based on the current or future plans for the project.
