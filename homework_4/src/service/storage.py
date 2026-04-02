import asyncio
from pathlib import Path
from uuid import uuid4

from botocore.exceptions import BotoCoreError, ClientError
from fastapi import Depends, HTTPException, UploadFile, status

from core.config import settings
from core.minio import get_minio_client


class StorageService:
    def __init__(self, client=Depends(get_minio_client)):
        self.bucket = settings.minio_bucket
        self.secure = settings.minio_secure
        self.endpoint = settings.minio_endpoint
        self.client = client

    async def upload_task_avatar(self, task_id: int, file: UploadFile) -> str:
        extension = Path(file.filename or "").suffix
        object_key = f"tasks/{task_id}/avatars/{uuid4().hex}{extension}"
        content = await file.read()

        if not content:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Файл пустой",
            )

        try:
            await asyncio.to_thread(
                self.client.put_object,
                Bucket=self.bucket,
                Key=object_key,
                Body=content,
                ContentType=file.content_type or "application/octet-stream",
            )
        except (BotoCoreError, ClientError) as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Не удалось загрузить файл в хранилище",
            ) from exc
        finally:
            await file.close()

        return f"{'https' if self.secure else 'http'}://{self.endpoint}/{self.bucket}/{object_key}"
