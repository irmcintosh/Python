1. **Open ArcGIS Pro Python Command Prompt**: 
   Start ArcGIS Pro and open the Python Command Prompt from the start menu.

2. **Create a Conda Virtual Environment**:
   ```sh
   conda create --name mbtile python=3.8
   ```
   Replace `3.8` with the Python version you prefer.

3. **Activate the Virtual Environment**:
   ```sh
   conda activate mbtile
   ```

4. **Install GDAL**:
   ```sh
   conda install -c conda-forge gdal
   ```

5. **Convert GeoTIFF to MBTiles using GDAL**:
   - Ensure you have your GeoTIFF file ready, let's assume it's named `input.tif`.
   - Use the following GDAL command to convert the GeoTIFF file to an MBTiles file:
   ```sh
   gdal_translate -of MBTILES input.tif output.mbtiles
   ```

### Complete Script:
```sh
# Open ArcGIS Pro Python Command Prompt

# Step 1: Create a conda virtual environment named mbtile
conda create --name mbtile python=3.8

# Step 2: Activate the mbtile environment
conda activate mbtile

# Step 3: Install GDAL in the mbtile environment
conda install -c conda-forge gdal

# Step 4: Convert GeoTIFF to MBTiles
gdal_translate -of MBTILES input.tif output.mbtiles
```

### Explanation:
- **Creating the environment**: `conda create --name mbtile python=3.8` creates a new virtual environment named `mbtile` with Python 3.8.
- **Activating the environment**: `conda activate mbtile` switches to the newly created environment.
- **Installing GDAL**: `conda install -c conda-forge gdal` installs GDAL from the conda-forge channel.
- **Converting the file**: `gdal_translate -of MBTILES input.tif output.mbtiles` uses the GDAL command-line tool to convert the input GeoTIFF file (`input.tif`) to an MBTiles file (`output.mbtiles`).

This workflow should help you set up your environment and perform the desired file conversion using GDAL. Let me know if you need further assistance or have any questions!
