import math


# Define constants for Earth's radius in meters
EARTH_RADIUS = 6371000  # meters

def preFocalLength(pixel_width, known_distance, known_width):
    return (pixel_width * known_distance)/known_width

def distance_to_camera(knownWidth, focalLength, perWidth):
    # Compute and return the distance from the object to the camera
    return (knownWidth * focalLength) / perWidth 


def calculate_new_lat_lon(camera_lat, camera_lon, distance, bearing):
    """
    Calculate a new latitude and longitude given the starting point (camera_lat, camera_lon),
    the distance to the new point, and the bearing (direction) to that point.

    Parameters:
    - camera_lat: Latitude of the camera
    - camera_lon: Longitude of the camera
    - distance: Distance to the object in meters
    - bearing: Bearing in degrees from the camera to the object (0 = North, 90 = East)

    Returns:
    - new_lat: Latitude of the new point
    - new_lon: Longitude of the new point
    """
    # Convert latitude, longitude, and bearing to radians
    lat1 = math.radians(camera_lat)
    lon1 = math.radians(camera_lon)
    bearing = math.radians(bearing)

    # Calculate new latitude
    new_lat = math.asin(math.sin(lat1) * math.cos(distance / EARTH_RADIUS) +
                        math.cos(lat1) * math.sin(distance / EARTH_RADIUS) * math.cos(bearing))

    # Calculate new longitude
    new_lon = lon1 + math.atan2(math.sin(bearing) * math.sin(distance / EARTH_RADIUS) * math.cos(lat1),
                                math.cos(distance / EARTH_RADIUS) - math.sin(lat1) * math.sin(new_lat))

    # Convert the results back to degrees
    new_lat = math.degrees(new_lat)
    new_lon = math.degrees(new_lon)

    return new_lat, new_lon


# Initialize the known distance from the camera to the object (73 meters)
known_distance = 22.2504
known_width = 0.762 # meter
pWidth = 0.047496855

# Latitude and Longitude of the camera 82.1907745°W 33.5782292°N 
camera_lat = 33.5782292
camera_lon = -82.1907745

# Example 
# Bearing examples for cardinal directions:
# North  (0°)   -> Directly in front of the camera (along the Earth's meridian line)
# East   (90°)  -> To the right of the camera (perpendicular to the north-south line)
# South  (180°) -> Directly behind the camera (opposite of north)
# West   (270°) -> To the left of the camera (opposite of east)
# Intermediate bearings:
# Northeast (45°), Southeast (135°), Southwest (225°), Northwest (315°)

bearing = 265  # Assuming the object is Northeast of the camera

focalLength = preFocalLength(pWidth, known_distance, known_width)

distance = distance_to_camera(known_width, focalLength, pWidth)


print(calculate_new_lat_lon(camera_lat, camera_lon, distance, bearing), distance, focalLength)
