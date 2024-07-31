import math
import arcpy
from arcpy.sa import *

def hata_okumura_model(frequency, ht, hr, distance, environment='urban'):
    def correction_factor(frequency, hr):
        return (1.1 * math.log10(frequency) - 0.7) * hr - (1.56 * math.log10(frequency) - 0.8)
    
    a_hr = correction_factor(frequency, hr)
    L_urban = (69.55 + 26.16 * math.log10(frequency) - 13.82 * math.log10(ht) 
               - a_hr + (44.9 - 6.55 * math.log10(ht)) * math.log10(distance))
    
    if environment == 'urban':
        return L_urban
    elif environment == 'suburban':
        L_suburban = L_urban - 2 * (math.log10(frequency / 28))**2 - 5.4
        return L_suburban
    elif environment == 'rural':
        L_rural = L_urban - 4.78 * (math.log10(frequency))**2 + 18.33 * math.log10(frequency) - 40.94
        return L_rural
    else:
        raise ValueError("Environment must be 'urban', 'suburban', or 'rural'")

# Define parameters
frequency = 900  # MHz
ht = 30  # Transmitting antenna height in meters
hr = 1.5  # Receiving antenna height in meters
environment = 'urban'  # Environment type

# Path to the input DEM
dem_path = "path/to/your/dem.tif"

# Coordinates of the antenna location (replace with actual coordinates)
antenna_location = (x, y)  # Replace with actual coordinates of the antenna

# Path to the output raster
out_raster_path = "path/to/output/path_loss.tif"

# Set environment settings
arcpy.env.workspace = "path/to/your/workspace"
arcpy.env.overwriteOutput = True

# Load DEM
dem = Raster(dem_path)

# Calculate distance from each pixel to the antenna location
distance_raster = EucDistance(dem, SourceData=antenna_location)

# Apply Hata-Okumura model
def apply_hata_okumura_model(distance_raster, frequency, ht, hr, environment):
    out_raster = Raster(distance_raster)
    with arcpy.da.UpdateCursor(out_raster, ["VALUE"]) as cursor:
        for row in cursor:
            distance = row[0] / 1000  # Convert distance to kilometers
            path_loss = hata_okumura_model(frequency, ht, hr, distance, environment)
            row[0] = path_loss
            cursor.updateRow(row)
    return out_raster

# Generate path loss raster
path_loss_raster = apply_hata_okumura_model(distance_raster, frequency, ht, hr, environment)

# Save the result
path_loss_raster.save(out_raster_path)

print(f"Path loss raster saved at {out_raster_path}")
