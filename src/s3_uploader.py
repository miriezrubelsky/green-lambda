import logging
import boto3
from config import Config

class S3Uploader:
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.s3_client = Config.get_s3_client()

    def upload_file(self, file_path, s3_key):
        """Uploads a file to S3."""
        try:
            self.s3_client.upload_file(file_path, self.bucket_name, s3_key)
            logging.info(f"File uploaded to S3 at {s3_key}")
        except Exception as e:
            logging.error(f"Error uploading file to S3: {e}")
            raise
