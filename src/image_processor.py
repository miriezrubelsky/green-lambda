import os
import numpy as np
from PIL import Image
import rasterio as rio
from io import BytesIO
from pathlib import Path

class ImageProcessor:
    def __init__(self, tif_data):
        self.tif_data = tif_data
    
    def tif_to_png(self, png_path):
        """Converts a TIF file to PNG."""
        with BytesIO(self.tif_data) as tif_file:
            with rio.open(tif_file) as src:
                array = src.read([1, 2, 3])  # Read the first three bands (RGB)
                rgb_array = np.dstack(array)  # Stack bands along the third dimension
                image = Image.fromarray(rgb_array, 'RGB')
                image.save(png_path)
    
    def split_image(self, image_path, out_folder, size: int, skip_empty: bool = False):
        """Splits an image into smaller chunks."""
        if not Path(out_folder).exists():
            Path(out_folder).mkdir(parents=True, exist_ok=True)

        image_name = Path(image_path).stem
        offsets = {}  # Dictionary to track offsets
        with Image.open(image_path) as img:
            width, height = img.size

            for i in range(0, width, size):
                for j in range(0, height, size):
                    box = (i, j, i + size, j + size)
                    crop = img.crop(box)
                    if skip_empty and np.sum(np.array(crop)) == 0:
                        continue
                     
                    crop_filename = f"{image_name}_{i}_{j}.png"
                    crop.save(os.path.join(out_folder, crop_filename))
                    offsets[crop_filename] = [i, j]  # Track the offset
        return offsets
