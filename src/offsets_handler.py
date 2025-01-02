import json
import os
import logging
from pathlib import Path


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class OffsetsHandler:
    
    def save_offsets(offsets, output_folder, image_name):
        if not Path(output_folder).exists():
            Path(output_folder).mkdir(parents=True, exist_ok=True)

        offsets_filename = f"{image_name}_offsets.txt"
        offsets_file_path = os.path.join(output_folder, offsets_filename)

        try:
            with open(offsets_file_path, 'w') as offsets_file:
                json_str = json.dumps(offsets, separators=(',', ':'))
                json_str = json_str.replace('],', '],\n')
                json_str = json_str.replace('{', '{\n').replace('}', '\n}')
                offsets_file.write(json_str)

            logger.info(f"Offsets saved to {offsets_file_path}")
            return offsets_file_path

        except Exception as e:
            logger.error(f"Error saving offsets to file: {e}")
            raise