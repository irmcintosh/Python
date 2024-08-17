import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter.font import Font

# Pre-defined lists for material and type choices
BRIDGE_MATERIALS = ['Concrete', 'Steel', 'Wood', 'Composite']
BRIDGE_TYPES = ['Beam', 'Arch', 'Suspension', 'Cable-stayed']

def calculate_bridge_load_capacity(length, width, height, material, bridge_type):
    """
    Advanced function to estimate the load capacity based on inputs.
    """
    base_capacity = 1000  # Base load capacity (arbitrary units)
    
    # Adjust capacity based on material
    if material == 'Concrete':
        base_capacity *= 1.5
    elif material == 'Steel':
        base_capacity *= 2.0
    elif material == 'Wood':
        base_capacity *= 0.5
    elif material == 'Composite':
        base_capacity *= 1.2

    # Adjust capacity based on bridge type
    if bridge_type == 'Beam':
        base_capacity *= 1.0
    elif bridge_type == 'Arch':
        base_capacity *= 1.8
    elif bridge_type == 'Suspension':
        base_capacity *= 2.5
    elif bridge_type == 'Cable-stayed':
        base_capacity *= 2.2

    # Length, width, and height might be factored in here
    adjusted_capacity = base_capacity * (length / 100) * (width / 10) * (height / 10)
    
    return adjusted_capacity

def assess_bridge_support():
    try:
        # Retrieve input values
        length = float(length_entry.get())
        width = float(width_entry.get())
        height = float(height_entry.get())
        material = material_combobox.get()
        bridge_type = type_combobox.get()
        vehicle_weight = float(vehicle_weight_entry.get())
        
        # Validate inputs
        if length <= 0 or width <= 0 or height <= 0 or vehicle_weight <= 0:
            raise ValueError("All numeric values must be greater than zero.")
        
        # Calculate bridge load capacity
        load_capacity = calculate_bridge_load_capacity(length, width, height, material, bridge_type)
        
        # Display the result
        if load_capacity >= vehicle_weight:
            result_message = f"The bridge can support the vehicle with a weight of {vehicle_weight} tons."
        else:
            result_message = f"The bridge cannot support the vehicle. Estimated load capacity: {load_capacity:.2f} tons."
        
        messagebox.showinfo("Assessment Result", result_message)
    except ValueError as e:
        messagebox.showerror("Input Error", str(e))

# Set up the main application window
app = tk.Tk()
app.title("Bridge Support Assessment Tool")
app.geometry("450x400")
app.resizable(False, False)

# Custom Font for the app
font_large = Font(family="Helvetica", size=12, weight="bold")
font_medium = Font(family="Helvetica", size=10)

# Header
ttk.Label(app, text="Bridge Support Assessment Tool", font=font_large).grid(column=0, row=0, columnspan=2, padx=10, pady=20)

# Length input
ttk.Label(app, text="Bridge Length (meters):", font=font_medium).grid(column=0, row=1, padx=10, pady=5, sticky="W")
length_entry = ttk.Entry(app)
length_entry.grid(column=1, row=1, padx=10, pady=5)

# Width input
ttk.Label(app, text="Bridge Width (meters):", font=font_medium).grid(column=0, row=2, padx=10, pady=5, sticky="W")
width_entry = ttk.Entry(app)
width_entry.grid(column=1, row=2, padx=10, pady=5)

# Height input
ttk.Label(app, text="Bridge Height Clearance (meters):", font=font_medium).grid(column=0, row=3, padx=10, pady=5, sticky="W")
height_entry = ttk.Entry(app)
height_entry.grid(column=1, row=3, padx=10, pady=5)

# Material selection
ttk.Label(app, text="Bridge Material:", font=font_medium).grid(column=0, row=4, padx=10, pady=5, sticky="W")
material_combobox = ttk.Combobox(app, values=BRIDGE_MATERIALS, state="readonly")
material_combobox.grid(column=1, row=4, padx=10, pady=5)
material_combobox.current(0)

# Type selection
ttk.Label(app, text="Bridge Type:", font=font_medium).grid(column=0, row=5, padx=10, pady=5, sticky="W")
type_combobox = ttk.Combobox(app, values=BRIDGE_TYPES, state="readonly")
type_combobox.grid(column=1, row=5, padx=10, pady=5)
type_combobox.current(0)

# Vehicle weight input
ttk.Label(app, text="Vehicle Weight (tons):", font=font_medium).grid(column=0, row=6, padx=10, pady=5, sticky="W")
vehicle_weight_entry = ttk.Entry(app)
vehicle_weight_entry.grid(column=1, row=6, padx=10, pady=5)

# Assess Button
assess_button = ttk.Button(app, text="Assess", command=assess_bridge_support)
assess_button.grid(column=0, row=7, columnspan=2, padx=10, pady=20)

# Run the application
app.mainloop()
