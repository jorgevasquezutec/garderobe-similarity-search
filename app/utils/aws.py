import boto3
import os
from PIL import Image
from io import BytesIO
from app.config.settings import aws_settings


__all__ = ("s3_client")

class s3Client:
    def __init__(self):
        self.access_key = aws_settings.AWS_S3_ACCESS_KEY_ID
        self.secret_key = aws_settings.AWS_S3_SECRET_ACCESS_KEY
        self.bucket_name = aws_settings.AWS_S3_BUCKET_NAME

    def load_image(self, image_key):
        s3 = boto3.client('s3', aws_access_key_id=self.access_key, aws_secret_access_key=self.secret_key)
        try:
            response = s3.get_object(Bucket=self.bucket_name, Key=image_key)
            image_data = response['Body'].read()
            image = Image.open(BytesIO(image_data))
            return image
        except Exception as e:
            print("Error loading image:", str(e))
            return None


s3_client = s3Client()
    