import arcpy

# Set up workspace and coordinate system
arcpy.env.workspace = r"C:\Users\Ian12724\Desktop\Miscellaneous\Drill\Military_Ground_Mobility\Scratch.gdb"
spatial_reference = arcpy.SpatialReference(3857)

# Create a point feature class for lattice points
point_fc = "LatticePoints"
arcpy.management.CreateFeatureclass(arcpy.env.workspace, point_fc, "POINT", spatial_reference=spatial_reference)

# Specify the extent of the lattice
desc = arcpy.Describe
xmin, ymin, xmax, ymax = (desc.extent.XMin,desc.extent.YMin, desc.extent.XMax, desc.extent.YMax)

# Create lattice points
with arcpy.da.InsertCursor(point_fc, ["SHAPE@XY"]) as ic:
    for x in range(int(xmin), int(xmax), 1000):
        for y in range(int(ymin), int(ymax), 1000):
            point = arcpy.Point(x, y)
            ic.insertRow([point])
print("Moing on to Edges")
# Create a line feature class for lattice edges
line_fc = "LatticeEdges"
arcpy.management.CreateFeatureclass(arcpy.env.workspace, line_fc, "POLYLINE", spatial_reference=spatial_reference)

# Create lattice edges
points = [row[0] for row in arcpy.da.SearchCursor(point_fc, "SHAPE@XY", spatial_reference=spatial_reference)]
with arcpy.da.InsertCursor(line_fc, ["SHAPE@"]) as cursor:
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            p1 = arcpy.PointGeometry(arcpy.Point(points[i][0], points[i][1]),spatial_reference)
            p2 = arcpy.PointGeometry(arcpy.Point(points[j][0], points[j][1]),spatial_reference)
            angle, distance = p1.angleAndDistanceTo(p2, 'PLANAR')
            
            if 0 < round(distance) <= 1500:
                print(distance)
                start1,end1,start2,end2 = [points[i][0],points[i][1],  points[j][0], points[j][1]]
                array = arcpy.Array([arcpy.Point(start1, end1), arcpy.Point(start2,end2)])
                line = arcpy.Polyline(array, spatial_reference=spatial_reference)
                cursor.insertRow((line,))
            #break

print("Lattice edges within 1000 meters created successfully.")