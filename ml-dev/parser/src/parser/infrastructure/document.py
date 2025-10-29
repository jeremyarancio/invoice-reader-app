from io import BytesIO
import os

from boto3 import client
from PIL import Image

from parser.service.ports.document import IDocumentRepository
from parser.settings import get_settings


settings = get_settings()


class S3DocumentRepository(IDocumentRepository):
    def __init__(self):
        self.s3_client = client("s3")
        self.bucket_name = settings.s3_bucket_name
        self.benchmark_document_s3_path = settings.benchmark_document_s3_path

    def get_document_image(self, image_name: str) -> Image.Image:
        img_data = self.s3_client.get_object(
            Bucket=self.bucket_name,
            Key=os.path.join(self.benchmark_document_s3_path, image_name),
        )["Body"].read()
        return Image.open(BytesIO(img_data))
