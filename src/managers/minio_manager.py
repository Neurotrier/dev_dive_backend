import uuid
from datetime import timedelta

from fastapi import UploadFile
from minio import Minio, S3Error

from src.core.config import settings
from src.core.logger import logger


class MinioManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(MinioManager, cls).__new__(cls)
        return cls._instance

    def __init__(
        self,
        endpoint: str = settings.MINIO_URL,
        access_key: str = settings.ACCESS_KEY,
        secret_key: str = settings.SECRET_KEY,
    ):
        if not hasattr(self, "initialized"):
            self.minio_client = Minio(
                endpoint=endpoint,
                access_key=access_key,
                secret_key=secret_key,
                secure=False,
            )
            self.create_bucket_if_not_exists()
            self.initialized = True

    def create_bucket_if_not_exists(self, bucket_name: str = settings.BUCKET_NAME):
        try:
            if not self.minio_client.bucket_exists(bucket_name):
                self.minio_client.make_bucket(bucket_name)
                logger.info(f"Bucket {bucket_name} was created")
            else:
                logger.info(f"Bucket '{bucket_name}' already exists.")
        except S3Error as e:
            logger.error(f"Error while creating bucket {bucket_name}")
            logger.error(str(e))

    async def upload_image(
        self,
        object_name: str,
        file: UploadFile,
        bucket_name: str = settings.BUCKET_NAME,
    ):
        self.minio_client.put_object(
            bucket_name,
            object_name,
            file.file,
            file.size,
            content_type=file.content_type,
        )
        return bucket_name + "/" + object_name

    def generate_presigned_url(
        self,
        object_name: str,
        bucket_name: str = settings.BUCKET_NAME,
        ttl: timedelta = timedelta(minutes=1),
    ):
        try:
            presigned_url = self.minio_client.presigned_get_object(
                bucket_name, object_name, expires=ttl
            )
            return presigned_url
        except Exception as e:
            logger.error(f"Error generating presigned URL for object {object_name}")
            logger.error(str(e))
            return None


minio_manager = MinioManager()
