from contextlib import asynccontextmanager
from typing import BinaryIO

from aiobotocore.session import get_session
from fastapi import UploadFile


class S3Client:
    def __init__(
            self,
            access_key: str,
            secret_key: str,
            endpoint_url: str,
            bucket_name: str,
    ):
        self.config = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "endpoint_url": endpoint_url,
        }
        self.bucket_name = bucket_name
        self.session = get_session()

    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client("s3", **self.config) as client:
            yield client

    async def upload_file(
            self,
            filename: str,
            file: UploadFile,
    ):
        async with self.get_client() as client:
            await client.put_object(
                Bucket=self.bucket_name,
                Key=filename,
                Body=file.file.read(),
            )

    async def upload_raw(
            self,
            filename: str,
            file: BinaryIO,
    ):
        async with self.get_client() as client:
            await client.put_object(
                Bucket=self.bucket_name,
                Key=filename,
                Body=file.read(),
            )

    async def delete_file(
            self,
            filename: str,
    ):
        async with self.get_client() as client:
            response = await client.delete_object(
                Bucket=self.bucket_name,
                Key=filename,
            )


async def upload_file(filename: str, file: UploadFile):
    s3_client = S3Client(
        access_key="1b607de15f004053b765358a3cc4be44",
        secret_key="42b176528a4f4c0b812934501cba94b6",
        endpoint_url="https://s3.storage.selcloud.ru",
        bucket_name="memento-memes-1"
    )

    await s3_client.upload_file(filename=filename, file=file)
    return f"https://5290a34f-703f-4fe3-a3d8-3f65685ed326.selstorage.ru/{filename}"


async def upload_raw(filename: str, file: BinaryIO):
    s3_client = S3Client(
        access_key="1b607de15f004053b765358a3cc4be44",
        secret_key="42b176528a4f4c0b812934501cba94b6",
        endpoint_url="https://s3.storage.selcloud.ru",
        bucket_name="memento-memes-1"
    )

    await s3_client.upload_raw(filename=filename, file=file)
    return f"https://5290a34f-703f-4fe3-a3d8-3f65685ed326.selstorage.ru/{filename}"


async def delete_file(filename: str):
    s3_client = S3Client(
        access_key="1b607de15f004053b765358a3cc4be44",
        secret_key="42b176528a4f4c0b812934501cba94b6",
        endpoint_url="https://s3.storage.selcloud.ru",
        bucket_name="memento-memes-1"
    )

    await s3_client.delete_file(filename=filename)

