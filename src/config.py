import boto3

class Config:
    # AWS credentials and configuration for S3
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

    REGION = 'us-west-2'  # Adjust region if needed


    metadata_output_folder = '/tmp/metadata_images'
    offsets_output_folder = '/tmp/offsets_images'
    split_output_folder = '/tmp/split_images'
    image_processing_offsets_path = 'output-splitted-png-in-process-offsets'
    image_processing_metadata_path = 'output-splitted-png-in-process-metadata'
    image_processing_path = 'output-splitted-png-in-process'
    
    @staticmethod
    def get_s3_client():
        return boto3.client(
            's3',
            aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
            region_name=Config.REGION
        )
