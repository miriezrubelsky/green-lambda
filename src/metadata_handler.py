import json
import rasterio as rio
from io import BytesIO
import os
from pathlib import Path

class MetadataHandler:
    @staticmethod
    def extract_metadata(tif_data):
        """Extracts metadata from a TIF file."""
        with rio.open(BytesIO(tif_data)) as src:
            transform = src.transform
            crs = src.crs
            image_size = src.read(1).shape  # Get the image size (width and height)
        
        metadata = {
            "transform": {
                "a": transform.a,
                "b": transform.b,
                "c": transform.c,
                "d": transform.d,
                "e": transform.e,
                "f": transform.f,
                "xoff": transform.xoff,
                "yoff": transform.yoff
            },
            "crs": crs.to_string(),
            "image_size": image_size[1]  # Width of the image (second dimension)
        }
        
        return metadata

    @staticmethod
    def save_metadata(metadata, output_folder, image_name):
        """Saves metadata to a file."""
        if not Path(output_folder).exists():
            Path(output_folder).mkdir(parents=True, exist_ok=True)
        metadata_filename = f"{image_name}_metadata.txt"
        metadata_file_path = os.path.join(output_folder, metadata_filename)

        try:
            with open(metadata_file_path, 'w') as metadata_file:
                json_str = json.dumps(metadata, separators=(',', ':'))
                json_str = json_str.replace(',', ',\n')
                json_str = json_str.replace('{', '{\n').replace('}', '\n}')
                metadata_file.write(json_str)

            return metadata_file_path
        except Exception as e:
            raise Exception(f"Error saving metadata: {e}")

    
