import arcpy
import time

# ========================== USER SETTINGS ==========================
point_fc = r"C:\Users\Ian12724\Desktop\Miscellaneous\Drill\WeaherOps2\WOE.gdb\Points"
outputgdb = r"C:\Users\Ian12724\Desktop\Miscellaneous\Drill\WeaherOps2\Slope.gdb"
pause = 2.0                                          # Seconds to pause between points
layer_name = "Points of Interest"                    # Exact layer name in Contents pane
# ===================================================================

# --- Initialize ArcGIS Pro project and active map view ----------------
aprx = arcpy.mp.ArcGISProject("CURRENT")
map_obj = aprx.activeMap
view = aprx.activeView                               # Requires map pane to have focus!
lyr = map_obj.listLayers(layer_name)[0]

# --- CAPTURE YOUR CURRENT VIEW AS THE TEMPLATE FOR ALL POINTS
# This records the exact extent (size + offset) you're looking at right now
template_extent = view.camera.getExtent()
template_sr = template_extent.spatialReference

print("Template view captured for consistent framing!")
print(f"   Approximate Scale: 1:{int(view.camera.scale):,}")
print(f"   Extent Width : {template_extent.width:,.0f} meters")
print(f"   Extent Height: {template_extent.height:,.0f} meters")
print(f"   Spatial Ref  : {template_sr.name}\n")

# --- Main loop: visit each point with identical framing ------------
count = 0
with arcpy.da.SearchCursor(lyr, ["SHAPE@XY", "id"]) as cursor:
    for row in cursor:
        count += 1
        x, y = row[0]                                # Coordinates of current point
        point_name = row[1]                          # Unique identifier (id/Name)
        safe_name = arcpy.ValidateTableName(str(point_name), outputgdb)

        print(f"{count:>3}: Flying to → {point_name}")

        # Rebuild the exact same extent window, but centered on current point
        half_width = template_extent.width / 2
        half_height = template_extent.height / 2

        new_extent = arcpy.Extent(
            XMin=x - half_width,
            YMin=y - half_height,
            XMax=x + half_width,
            YMax=y + half_height,
            spatial_reference=template_sr
        )

        # Apply your perfect custom view to the map
        view.camera.setExtent(new_extent)

        # Highlight the current point
        where_clause = f"id = '{point_name}'" if isinstance(point_name, str) else f"id = {point_name}"
        arcpy.management.SelectLayerByAttribute(lyr, "NEW_SELECTION", where_clause)

        # Extract raster value(s) using the exact same analysis window
        out_fc = f"{outputgdb}\\{safe_name}"
        with arcpy.EnvManager(extent=new_extent):
            arcpy.sa.ExtractValuesToPoints(
                in_point_features=lyr,
                in_raster=r"Elevation\DEM03_slope",
                out_point_features=out_fc,
                interpolate_values="INTERPOLATE",
                add_attributes="VALUE_ONLY"
            )

        # Report extracted slope value
        with arcpy.da.SearchCursor(out_fc, "RASTERVALU") as val_cur:
            slope_value = val_cur.next()[0]
        print(f"      Slope = {slope_value:.2f}°")

        time.sleep(pause)  # Pause so you can enjoy the view
        
        # === Remove the temporary output layer from the Contents pane ===
        # Find it by its name and remove it so the Contents pane stays clean.
        temp_layers = map_obj.listLayers(safe_name)
        for temp_lyr in temp_layers:
            try:
                map_obj.removeLayer(temp_lyr)
                print(f"     Removed temporary layer '{safe_name}' from map")
            except Exception as e:
                print(f"     Could not remove layer '{safe_name}': {e}")

        # Clean up selection for next iteration
        arcpy.management.SelectLayerByAttribute(lyr, "CLEAR_SELECTION")

# =====================================================================
print(f"\nTour complete! Processed {count} points with identical custom framing.")
print("All outputs saved to:", outputgdb)
