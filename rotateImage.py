from PIL import Image

# Open the image
img = Image.open("/mnt/data/snapshot_0000.png")

# Rotate the image 180 degrees
rotated_img = img.rotate(180)

# Save the corrected version
rotated_img.save("/mnt/data/snapshot_0000_rotated.png")

# Show it (optional)
rotated_img.show()
