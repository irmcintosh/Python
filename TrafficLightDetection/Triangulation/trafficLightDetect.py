import os
import json
import cv2
from math import *
import numpy as np
import itertools
import pandas as pd
import zipfile
from pathlib import Path
from arcgis.geometry import Point
from arcgis.geometry import Geometry


from ultralytics import YOLO  # Import YOLO from ultralytics because arcgis learn modules errors out

# Download & setup data (same as before)
from arcgis.gis import GIS

# gis = GIS("home")
# oriented_imagery_data = gis.content.get("d606e6827c8746e383de96d8718be9a8")
sampleDir = r"C:\Users\Ian12724\Desktop\Esri\Desktop_Demo\TrafficLightDetection\sample"
# Download sample data
# filepath = oriented_imagery_data.download(save_path=sampleDir, 
#                                           file_name=oriented_imagery_data.name)

# with zipfile.ZipFile(filepath, 'r') as zip_ref:
#     zip_ref.extractall(Path(filepath).parent)



filepath = r'C:\Users\Ian12724\Desktop\Esri\Desktop_Demo\TrafficLightDetection\sample\oriented_imagery_sample_notebook'

data_path = Path(os.path.join(os.path.splitext(filepath)[0]), "street_view_data")
image_meta_data = Path(os.path.join(os.path.splitext(filepath)[0]), "oriented_imagery_meta_data.csv")
image_path_list = [os.path.join(data_path, image) for image in os.listdir(data_path)]

# Model loading (using Ultralytics YOLOv3)
yolo = "yolov9e.pt"
model = YOLO(yolo)  # Load a pretrained YOLOv3 model
# Model inferencing (modified for Ultralytics)
def traffic_light_finder(oriented_image_path):
    flag = 0
    coordlist = []
    temp_list = {}
    results = model(oriented_image_path, conf=0.65)  # Perform inference

    test_img = cv2.imread(oriented_image_path)

    if not results[0].boxes: #check if any object was detected.
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
                    b = box.xyxy[0].cpu().numpy().astype(int)  # get box coordinates in (left, top, right, bottom) format
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

# Create output location
marked_image_saved_folder = os.path.join(sampleDir, f"traffic_light_marked_{yolo[:-3]}")
os.makedirs(marked_image_saved_folder, exist_ok=True)
print("Path created for saving the images with traffic light detected on them : - ", marked_image_saved_folder)

detections = {}
for e, image in enumerate(image_path_list):
    try:
        val_dict, out_image = traffic_light_finder(image)
        if bool(val_dict):
            detections[os.path.basename(image)] = val_dict
            cv2.imwrite(os.path.join(marked_image_saved_folder, os.path.basename(image)), out_image)
    except Exception as e:
        print(e)
detections ={key: value for key, value in detections.items() if value.get('object') is True}
print(detections)

with open(r"C:\Users\Ian12724\Desktop\Esri\Desktop_Demo\TrafficLightDetection\sample\oriented_imagery_sample_notebook\traffic_light_data_sample.json",
           "w") as f:
    json.dump(detections, f)


camera_df = pd.read_csv(image_meta_data)

dets = list(detections.keys())

def find_intersection(
    x1,
    y1,
    x2,
    y2,
    x3,
    y3,
    x4,
    y4,
):
    px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / (
        (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    )
    py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / (
        (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    )
    return [px, py]


def ccw(A, B, C):
    return (C.y - A.y) * (B.x - A.x) > (B.y - A.y) * (C.x - A.x)


def intersect(A, B, C, D):
    return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)


class dotdict(dict):
    """dot.notation access to dictionary attributes"""

    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


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

(H, W, _) = cv2.imread(image_path_list[0]).shape
points = []
meta_data= []

for i in range(len(dets) - 1):  # check coordinates of two consecutive images
    # load data of image1
    img1 = (dets[i])[:-7]
    cam1 = camera_df[camera_df["Name"] == img1].to_dict("records")[0] if bool(camera_df[camera_df["Name"] == img1].to_dict("records")) else False
    if not bool(cam1):
        continue
        
    bboxes1 = detections[img1 + "_cp.tif"]["coords"]

    # load data of image2

    img2 = (dets[i + 1])[:-7]
    cam2 = camera_df[camera_df["Name"] == img2].to_dict("records")[0]
    bboxes2 = detections[img2 + "_cp.tif"]["coords"]

    DIST = cam1["FarDist"]

    for bbox1 in bboxes1:  # loop over all the bbox in image1
        if bbox1[3] > 50:  # ignore small bboxes
            
            x1_0 = eval(cam1["SHAPE"])["x"]
            y1_0 = eval(cam1["SHAPE"])["y"]
            
            # calculate the angle of the object in image1
            direction_angle1 = cam1["CamHeading"] + cam1["HFOV"] / 2.0 * (
                (bbox1[0] + bbox1[2] / 2) - W / 2.0
            ) / (W / 2.0)
            angle_subtended_by_object1 = cam1["VFOV"] * bbox1[3] / H
            
            # calculate the distance where the object is based on angle
            x1_1 = eval(cam1["SHAPE"])["x"] + DIST * cos(
                pi / 2 - radians(direction_angle1)
            )
            y1_1 = eval(cam1["SHAPE"])["y"] + DIST * sin(
                pi / 2 - radians(direction_angle1)
            )

            for bbox2 in bboxes2:  # loop over all the bbox in image2
                if bbox2[3] > 50:  # ignore small bboxes

                    x2_0 = eval(cam2["SHAPE"])["x"]
                    y2_0 = eval(cam2["SHAPE"])["y"]
                    
                    # calculate the angle of the object in image2
                    direction_angle2 = cam2["CamHeading"] + cam2["HFOV"] / 2.0 * (
                        bbox2[0] + bbox2[2] / 2 - W / 2.0
                    ) / (W / 2.0)
                    angle_subtended_by_object2 = cam2["VFOV"] * bbox2[3] / H
                    
                    # calculate the distance where the object is based on angle
                    x2_1 = eval(cam2["SHAPE"])["x"] + DIST * cos(
                        pi / 2 - radians(direction_angle2)
                    )
                    y2_1 = eval(cam2["SHAPE"])["y"] + DIST * sin(
                        pi / 2 - radians(direction_angle2)
                    )
                    
                    # find if the line intersects
                    val = intersect(
                        dotdict({"x": x1_0, "y": y1_0}),
                        dotdict({"x": x1_1, "y": y1_1}),
                        dotdict({"x": x2_0, "y": y2_0}),
                        dotdict({"x": x2_1, "y": y2_1}),
                    )
                    xmin, ymin, xmax, ymax = (
                        bbox2[0],
                        bbox2[1],
                        bbox2[0] + bbox2[2],
                        bbox2[1] + bbox2[3],
                    )
                    
                    # find the point where line from image1 and image2 intersect
                    if val:
                        midpoint = find_intersection(
                            x1_0, y1_0, x1_1, y1_1, x2_0, y2_0, x2_1, y2_1
                        )
                        points.append(midpoint)
                        meta_data.append(
                            {
                                "image1": img1,
                                "image2": img2,
                                "points": midpoint,
                                "coords": [xmin, ymin, xmax, ymax],
                                "x": midpoint[0],
                                "y": midpoint[1],
                            }
                        )

print(f'Number of traffic lights extracted - {len(points)}')
outpoints = process(points)
print (f'Number of traffic lights extracted after clustering and removing redundant traffic light - {len(outpoints)}')                        

out_meta_data = []
for e,i in enumerate(points):
    if i in outpoints:
        out_meta_data.append(meta_data[e])

# creating a spatial dataframe and exporting as feature class
spatial_df = []
for e, i in enumerate(out_meta_data):
    tempdict = {}
    tempdict["X"] = i["x"]
    tempdict["Y"] = i["y"]
    tempdict["Z"] = 100
    tempdict["ImgUrn"] = str(
        i["image2"][1:]
        + "|VilniusCity_ExposurePoints|"
        + str(
            camera_df[camera_df["Name"] == i["image2"]].to_dict("records")[0][
                "OBJECTID"
            ]
        )
    )
    tempdict["ImgGeom"] = json.dumps(
        {
            "xmin": i["coords"][0],
            "ymin": i["coords"][1],
            "xmax": i["coords"][2],
            "ymax": i["coords"][3],
            "pos": "BC",
        }
    )
    tempdict["Labels"] = "traffic lights"
    tempdict["SHAPE"] = Geometry(
        {
            "x": i["x"],
            "y": i["y"],
            "spatialReference": {"wkid": 3857, "latestWkid": 102100},
        }
    )
    spatial_df.append(tempdict)

    
df = pd.DataFrame(data=spatial_df)
df.spatial.set_geometry("SHAPE")
print(df)
# exporting the layer on ArcGIS Online org
gdb = r'C:\Users\Ian12724\Desktop\Esri\Desktop_Demo\TrafficLightDetection\DeepLearning.gdb'
df.spatial.to_featureclass(os.path.join(gdb,f"exported_traffic_points_{yolo[:-3]}"), sanitize_columns=False)
