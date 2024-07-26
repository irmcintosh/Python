# Roadway Management Tool Demo

## Overview

The Roadway Management Tool Demo is a custom ArcGIS Python toolbox designed to calibrate route measures for polyline feature layers. It includes a single tool, "Calibrate Routes," that allows users to update the M-values (measure values) of polyline features based on specified measures or feature attributes.

## Files

- `roadway_management_tool_demo.pyt`: The Python toolbox file containing the tool definition and logic.

## Installation

1. Clone the repository or download the `.pyt` file.
2. Open ArcGIS Pro.
3. In the Catalog pane, right-click on "Toolboxes" and select "Add Toolbox".
4. Navigate to the location of the `.pyt` file and add it.

## Usage

1. In ArcGIS Pro, open the toolbox from the Catalog pane.
2. Double-click on the "Calibrate Routes" tool to open the tool dialog.
3. Fill in the required parameters and run the tool.

## Parameters

### Input Route Layer

- **Name:** `input_route`
- **Data Type:** `GPFeatureLayer`
- **Description:** The input polyline feature layer that contains the routes to be calibrated.
- **Required:** Yes

### From Measure

- **Name:** `from_measure`
- **Data Type:** `GPDouble`
- **Description:** The measure value to assign to the first vertex of the polyline.
- **Required:** Optional (required if `use_attribute` is False)

### To Measure

- **Name:** `to_measure`
- **Data Type:** `GPDouble`
- **Description:** The measure value to assign to the last vertex of the polyline.
- **Required:** Optional (required if `use_attribute` is False)

### Use Feature Attribute

- **Name:** `use_attribute`
- **Data Type:** `GPBoolean`
- **Description:** A boolean flag indicating whether to use feature attributes for the measures.
- **Required:** Yes

### From Measure Field - Route Layer

- **Name:** `attr_from_measure`
- **Data Type:** `Field`
- **Description:** The field in the input route layer that contains the from measure values.
- **Required:** Optional (required if `use_attribute` is True)

### To Measure Field - Route Layer

- **Name:** `attr_to_measure`
- **Data Type:** `Field`
- **Description:** The field in the input route layer that contains the to measure values.
- **Required:** Optional (required if `use_attribute` is True)

## Functions

### distance(point1, point2)

Calculates the Euclidean distance between two points.

- **Parameters:**
  - `point1` (list): Coordinates of the first point [x, y].
  - `point2` (list): Coordinates of the second point [x, y].
- **Returns:**
  - `float`: The distance between the two points.

### interpolate_distances(points)

Interpolates the distances between a series of points and updates their measure values.

- **Parameters:**
  - `points` (list): A list of points with [x, y, measure] values.
- **Returns:**
  - `list`: A list of points with updated measure values.

### update_geometry_with_measures(polyline, measures)

Updates the geometry of a polyline feature with the given measure values.

- **Parameters:**
  - `polyline` (arcpy.Polyline): The input polyline feature.
  - `measures` (list): A list of measure values.
- **Returns:**
  - `arcpy.Polyline`: The updated polyline feature.

## Tool Class Definitions

### Toolbox

Defines the toolbox.

- **Attributes:**
  - `label` (str): The label for the toolbox.
  - `alias` (str): The alias for the toolbox.
  - `tools` (list): A list of tool classes associated with this toolbox.

### CalibrateRoutes

Defines the "Calibrate Routes" tool.

- **Attributes:**
  - `label` (str): The label for the tool.
  - `description` (str): The description of the tool.
  - `canRunInBackground` (bool): Indicates whether the tool can run in the background.

- **Methods:**
  - `updateParameters(parameters)`: Modifies parameters based on the value of the `use_attribute` parameter.
  - `getParameterInfo()`: Defines parameter definitions.
  - `execute(parameters, messages)`: Executes the tool logic to calibrate route measures.

## Example Usage

### Using Direct Measures

1. Select the input route layer.
2. Set the `From Measure` and `To Measure` values.
3. Ensure `Use Feature Attribute` is unchecked.
4. Run the tool.

### Using Feature Attributes

1. Select the input route layer.
2. Check the `Use Feature Attribute` option.
3. Select the fields for `From Measure Field - Route Layer` and `To Measure Field - Route Layer`.
4. Run the tool.

## Logging

The tool provides detailed logging messages in the ArcGIS Pro Geoprocessing pane, including the status of the calibration process and the updated measure values for each polyline.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome. Please open an issue or submit a pull request for any improvements or bug fixes.

---

This documentation provides a comprehensive guide to understanding, installing, and using the Roadway Management Tool Demo. If you have any questions or need further assistance, feel free to open an issue in the repository.
