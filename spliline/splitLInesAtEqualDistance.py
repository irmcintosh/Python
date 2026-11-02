import arcpy

def split_polyline_with_equal_distance(input_polyline, output_feature_class, distance):
    import os
    # Create a feature layer from the input polyline
    arcpy.MakeFeatureLayer_management(input_polyline, "input_layer")
    
    # Create Point Feature for Spliting Line
    gdbPath = os.path.dirname(output_feature_class)
    pointLayer = arcpy.management.CreateFeatureclass(gdbPath, "PointLayer_", 'POINT')

    # Get the length of the input polyline
    length_field = arcpy.AddFieldDelimiters("input_layer", "Shape_Length")
    expression = "!{}!".format(length_field)
    total_length = sum(row[0] for row in arcpy.da.SearchCursor("input_layer", ["Shape_Length"]))

    # Calculate the number of segments needed
    num_segments = int(total_length / distance)

    # Create a list to store the split points
    split_points = []

    # Iterate through the segments and calculate split points
    for i in range(1, num_segments):
        distance_along_line = i * distance
        expression = "{} >= 0 AND {} <= {}".format(length_field, distance_along_line - distance / 2, distance_along_line + distance / 2)

        with arcpy.da.SearchCursor("input_layer", ["SHAPE@"], where_clause=expression) as cursor:
            for row in cursor:
                split_points.append(row[0].positionAlongLine(distance_along_line).firstPoint)
    with arcpy.da.InsertCursor(pointLayer, ["SHAPE@XY"]) as insertCur:
        for point in split_points:
            insertCur.insertRow([point])
    # Use the split points to split the polyline
    arcpy.SplitLineAtPoint_management("input_layer",pointLayer, output_feature_class, f"{distance} meters")
