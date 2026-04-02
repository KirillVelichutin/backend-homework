import boto3

from core.config import settings


MINIO_URL = f"{'https' if settings.minio_secure else 'http'}://{settings.minio_endpoint}"

client = boto3.client(
    "s3",
    endpoint_url=MINIO_URL,
    aws_access_key_id=settings.minio_access_key,
    aws_secret_access_key=settings.minio_secret_key,
)


def get_minio_client():
    try:
        yield client
    finally:
        pass
