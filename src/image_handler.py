import os
import json
import urllib.parse
from pathlib import Path
from image_processor import ImageProcessor
from metadata_handler import MetadataHandler
from offsets_handler import OffsetsHandler
from s3_uploader import S3Uploader
from config import Config

class ImageHandler:
    def __init__(self, event, context):
        self.event = event
        self.context = context
        self.bucket_name = event['Records'][0]['s3']['bucket']['name']
        self.image_key = event['Records'][0]['s3']['object']['key']
        self.s3_uploader = S3Uploader(self.bucket_name)
    
    def decode_image_key(self):
        """Decodes the image key from the event."""
        return urllib.parse.unquote(self.image_key)

    def fetch_image(self):
        """Fetches the image from S3."""
        decoded_key = self.decode_image_key()
        s3_client = Config.get_s3_client()
        response = s3_client.get_object(Bucket=self.bucket_name, Key=decoded_key)
        return response['Body'].read()

    def process_image(self, tif_data):
        """Processes the image: converts it and splits it."""
        processor = ImageProcessor(tif_data)
        png_path = '/tmp/' + Path(self.image_key).stem + '.png'
        processor.tif_to_png(png_path)
        split_size = 1600
        offsets = processor.split_image(png_path, Config.split_output_folder, split_size)
        return png_path, offsets
    
  

    def process(self):
        """Main image handling logic."""
        tif_data = self.fetch_image()
        metadata = MetadataHandler.extract_metadata(tif_data)
        png_path, offsets = self.process_image(tif_data)
        image_name = Path(png_path).stem
        metadata_file_path = MetadataHandler.save_metadata(metadata, Config.metadata_output_folder, image_name)
        offsets_file_path = OffsetsHandler.save_offsets(offsets, Config.offsets_output_folder, image_name)
        for filename, _ in offsets.items():
            split_image_path = os.path.join(Config.split_output_folder, filename)
            #image_processing_path = 'output-splitted-png-in-process'
            s3_key = f'{Config.image_processing_path}/{image_name}/{filename}'
            self.s3_uploader.upload_file(split_image_path, s3_key)
        s3_key_offsets = f'{Config.image_processing_offsets_path}/{image_name}_offsets.txt'
        self.s3_uploader.upload_file(offsets_file_path, s3_key_offsets)
        #image_processing_metadata_path = 'output-splitted-png-in-process-metadata'
        s3_key_metadata = f'{Config.image_processing_metadata_path}/{image_name}_metadata.txt'
        self.s3_uploader.upload_file(metadata_file_path, s3_key_metadata)

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'File fetched and converted successfully'}),
            'headers': {'Content-Type': 'application/json'}
        }
