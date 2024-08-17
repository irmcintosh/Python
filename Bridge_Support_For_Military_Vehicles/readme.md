# Bridge Support Assessment Tool

This is a Python application with a graphical user interface (GUI) built using `tkinter`. The tool allows users to assess whether a specific bridge can support a military vehicle based on the bridge's dimensions, material, and type, as well as the vehicle's weight.

## Features

- **User-friendly GUI**: A clean and intuitive interface for entering bridge and vehicle parameters.
- **Real-time Validation**: Immediate feedback if input values are incorrect or invalid.
- **Load Capacity Calculation**: The application estimates the bridge's load capacity based on the provided inputs and determines if it can support the given vehicle.
- **Results Display**: The result of the assessment is displayed in a pop-up message box.

## Requirements

- Python 3.x
- `tkinter` (usually included with Python)

## Usage

1. **Clone or Download the Repository**:
   ```
   git clone <repository-url>
   ```

2. **Run the Application**:
   ```
   python bridge_assessment_gui.py
   ```

3. **Input Parameters**:
   - **Bridge Length**: Enter the length of the bridge in meters.
   - **Bridge Width**: Enter the width of the bridge in meters.
   - **Height Clearance**: Enter the height clearance of the bridge in meters.
   - **Material**: Select the material of the bridge (Concrete, Steel, Wood, Composite).
   - **Type**: Select the type of the bridge (Beam, Arch, Suspension, Cable-stayed).
   - **Vehicle Weight**: Enter the weight of the vehicle in tons.

4. **Assess**:
   - Click the "Assess" button to calculate and display whether the bridge can support the vehicle.

## License

This project is licensed under the MIT License.

## Contribution

Feel free to submit issues, fork the repository, and make pull requests. Contributions are welcome!
