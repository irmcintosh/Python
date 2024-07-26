import arcpy
import numpy as np

# Define the distance function
def distance(point1, point2):
    return np.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)


def interpolate_distances(points):
    interpolated_points = []
    total_distance = 0.0
    cumulative_distances = [0.0]

    # Calculate cumulative distances and total distance
    for i in range(1, len(points)):
        dist = distance(points[i - 1], points[i])
        total_distance += dist
        cumulative_distances.append(total_distance)

    # Sort points based on cumulative distances
    sorted_points = [point for _, point in sorted(zip(cumulative_distances, points))]

    # Linearly interpolate distances
    for i in range(1, len(sorted_points)):
        sorted_points[i][2] = np.interp(
            cumulative_distances[i],
            [0, total_distance],
            [sorted_points[0][2], sorted_points[-1][2]]
        )
        interpolated_points.append(sorted_points[i])

    return interpolated_points

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
            # Update the M value of the point
            point.M = measure
            updated_geometry.add(point)
    
    # Create a new Polyline object with the updated geometry
    updated_polyline = arcpy.Polyline(updated_geometry)
    
    return updated_polyline
class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Roadway Management Tool Demo"
        self.alias = "Roadway Management Tool Demo"
        # List of tool classes associated with this toolbox
        self.tools = [CalibrateRoutes]

class CalibrateRoutes(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Calibrate Routes"
        self.description = "Calibrate route measures."
        self.canRunInBackground = False
    def updateParameters(self, parameters):
        """Modify parameters based on the value of the use_attribute parameter"""
        
        if parameters[3].value:  # If use_attribute is True
            parameters[2].enabled = False  # To Measure parameter disabled
            parameters[1].enabled = False  # From Measure parameter disabled
            parameters[4].enabled = True   # Field parameter enabled
            parameters[5].enabled = True   # Field parameter enabled
            parameters[4].parameterType = 'Required'
            parameters[5].parameterType = 'Required'
        else:  # If use_attribute is False
            parameters[2].enabled = True   # To Measure parameter enabled
            parameters[1].enabled = True   # From Measure parameter enabled
            parameters[4].enabled = False  # Field parameter disabled
            parameters[5].enabled = False  # Field parameter disabled
            parameters[1].parameterType = 'Required'
            parameters[2].parameterType = 'Required'

        return
    def getParameterInfo(self):
        """Define parameter definitions"""
        
        # Parameter 1: Input polyline feature layer
        param0 = arcpy.Parameter(
            displayName="Input Route Layer",
            name="input_route",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input")

        # Parameter 2: From measure
        param1 = arcpy.Parameter(
            displayName="From Measure",
            name="from_measure",
            datatype="GPDouble",
            parameterType="Optional",
            direction="Input")

        # Parameter 3: To measure
        param2 = arcpy.Parameter(
            displayName="To Measure",
            name="to_measure",
            datatype="GPDouble",
            parameterType="Optional",
            direction="Input")
        
        # Parameter 4: Boolean checkbox - Use feature attribute
        param3 = arcpy.Parameter(
            displayName="Use Feature Attribute",
            name="use_attribute",
            datatype="GPBoolean",
            parameterType="Required",
            direction="Input")
        param3.value = False
        param3.filter.type = "ValueList"
        param3.filter.list = ['True', 'False']
        
        # Parameter 5: Optional input - Start point field
        
        param4 = arcpy.Parameter(
            displayName= f"From Measure Field - Route Layer",
            name="attr_from_measure",
            datatype="Field",
            parameterType="Optional",
            direction="Input")
        param4.parameterDependencies = [param0.name]

        # Parameter 6: Optional input - End point field
        param5 = arcpy.Parameter(
            displayName=f"To Measure Field - Route Layer",
            name="attr_to_measure",
            datatype="Field",
            parameterType="Optional",
            direction="Input")
        param5.parameterDependencies = [param0.name]

        return [param0, param1, param2, param3, param4, param5]

    def execute(self, parameters, messages):
        """Calibrate route measures"""

        # Get input parameters
        in_polyline = parameters[0].valueAsText
        from_measure_ = parameters[1].value
        to_measure_ = parameters[2].value
        use_attribute = parameters[3].value        
        # Get optional input - Attribute From Meas
        attr_from_meas = parameters[4].valueAsText if parameters[4].value else None
        # Get optional input - Attribute To Meas
        attr_to_meas = parameters[5].valueAsText if parameters[5].value else None
        attr = 'True' if use_attribute else 'False'
        arcpy.AddMessage(f'Starting to calibrate M-Values for {in_polyline}')


        # Perform calibration operations here
        count =1
        if not use_attribute:
            
            arcpy.AddMessage(f'|{"Item":<10} |{"From Measure":<10} | {"To Measure":<10} | {"Use Attribute":<10} | {"Status":<10} | {"Vertices with M-Values":<10} |')
            # Create an update cursor to iterate over the polylines
            with arcpy.da.UpdateCursor(in_polyline, ["SHAPE@"]) as cursor:
                arcpy.AddMessage(f'|{count:<10} | {in_polyline:<15} | {from_measure_:<15} | {to_measure_:<15} | {attr:<15} | {"Processing":<15} | {"[]":<22} |')
                for row in cursor:
                    polyline = row[0]
                    
                    # Get the vertices of the polyline
                    vertices = [[point.X, point.Y, None] for part in polyline for point in part]
                    arcpy.AddMessage(f'|{count:<10} |{from_measure_:<10} | {to_measure_:<15} | {attr:<15} | {"Processing":<15} | {str(len(vertices)):<22} |')
                    # Add from_measure to the first vertex and to_measure to the last vertex
                    vertices[0][2] = from_measure_
                    vertices[-1][2] = to_measure_
                    
                    # Interpolate distances and update measures
                    interpolated_points = interpolate_distances(vertices)
                    interpolated_points = [vertices[0]] + interpolated_points
                    measures = [point[2] for point in interpolated_points]
                    arcpy.AddMessage(f'|{count:<10} |{from_measure_:<15} | {to_measure_:<15} | {attr:<15} | {"Updated":<15} | {str(measures):<50} |')
                    # Update geometry with measure values
                    updated_polyline = update_geometry_with_measures(polyline, measures)
                    
                    # Update the geometry of the feature
                    cursor.updateRow([updated_polyline])
                    count +=1

                arcpy.AddMessage(f'|{from_measure_:<10} | {to_measure_:<15} | {attr:<15} | {"Calibrated":<15} | {str(measures):<50} |')
        else:
            arcpy.AddMessage(f'|{"Item":<10} |{"From Measure":<15} | {"To Measure":<15} | {"Use Attribute":<15} | {"Status":<15} | {"Vertices with M-Values":<10} |')
            # Create an update cursor to iterate over the polylines
            with arcpy.da.UpdateCursor(in_polyline, ["SHAPE@", attr_from_meas, attr_to_meas]) as cursor:
                
                for row in cursor:
                    polyline = row[0]
                    from_measure = row[1]
                    to_measure = row[2]
                    arcpy.AddMessage(f'|{count:<10} |{from_measure:<15} | {to_measure:<15} | {attr:<15} | {"Processing":<15} | {"[]":<22} |')
                    # Get the vertices of the polyline
                    vertices = [[point.X, point.Y, None] for part in polyline for point in part]
                    arcpy.AddMessage(f'|{count:<10} |{from_measure:<15} | {to_measure:<15} | {attr:<15} | {"Processing":<15} | {str(len(vertices)):<22} |')
                    # Add from_measure to the first vertex and to_measure to the last vertex
                    vertices[0][2] = from_measure
                    vertices[-1][2] = to_measure
                    
                    # Interpolate distances and update measures
                    interpolated_points = interpolate_distances(vertices)
                    interpolated_points = [vertices[0]] + interpolated_points
                    measures = [point[2] for point in interpolated_points]
                    arcpy.AddMessage(f'|{count:<10} |{from_measure:<15} | {to_measure:<15} | {attr:<15} | {"Updated":<15} | {str(measures):<50} |')
                    # Update geometry with measure values
                    updated_polyline = update_geometry_with_measures(polyline, measures)
                    
                    # Update the geometry of the feature
                    cursor.updateRow([updated_polyline, from_measure, to_measure])
                    
                    arcpy.AddMessage(f'|{count:<10} |{from_measure:<15} | {to_measure:<15} | {attr:<15} | {"Calibrated":<15} | {str(measures):<50} |')
                    arcpy.AddMessage('='*145)
                    count+=1

        return
