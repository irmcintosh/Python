import arcpy
import numpy as np

# Define the distance function
def distance(point1, point2):
    return np.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)

# Define the interpolate_distances function
def interpolate_distances(points):
    interpolated_points = []
    total_distance = 0.0
    
    # Calculate cumulative distances and total distance
    for i in range(1, len(points)):
        dist = distance(points[i-1], points[i])
        total_distance += dist
        interpolated_points.append([points[i][0], points[i][1], total_distance])
    
    # Linearly interpolate distances
    for i in range(1, len(interpolated_points)):
        interpolated_points[i][2] = np.interp(
            interpolated_points[i][2],
            [0, total_distance],
            [points[0][2], points[-1][2]]
        )
    
    return interpolated_points

# Function to update geometry with measure values
def update_geometry_with_measures(polyline, measures):
    # Create a new array to hold the updated geometry
    updated_geometry = arcpy.Array()
    
    # Loop through each part of the polyline
    for part in polyline:
        # Loop through each vertex in the part
        for i in range(part.count):
            point = part.getObject(i)
            # Get the measure value for this vertex
            measure = measures[i] if i < len(measures) else None
            # Update the Z value of the point
            point.M = measure
            updated_geometry.add(point)
    
    # Create a new Polyline object with the updated geometry
    updated_polyline = arcpy.Polyline(updated_geometry)
    
    return updated_polyline

# Get the polyline feature class and field names
polyline_fc = r"Road_Segments"
from_measure_field = 'frommeasure'
to_measure_field = "tomeasure"

# Create an update cursor to iterate over the polylines
with arcpy.da.UpdateCursor(polyline_fc, ["SHAPE@", from_measure_field, to_measure_field]) as cursor:
    for row in cursor:
        polyline = row[0]
        from_measure = row[1]
        to_measure = row[2]
        
        # Get the vertices of the polyline
        vertices = [[point.X, point.Y, None] for part in polyline for point in part]
        
        # Add from_measure to the first vertex and to_measure to the last vertex
        vertices[0][2] = from_measure
        vertices[-1][2] = to_measure
        
        # Interpolate distances and update measures
        interpolated_points = interpolate_distances(vertices)
        interpolated_points = [vertices[0]] + interpolated_points
        measures = [point[2] for point in interpolated_points]
        
        # Update geometry with measure values
        updated_polyline = update_geometry_with_measures(polyline, measures)
        
        # Update the geometry of the feature
        cursor.updateRow([updated_polyline, from_measure, to_measure])

print("Geometry updated with measure values.")

