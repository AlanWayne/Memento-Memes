from contextlib import asynccontextmanager
from os import environ
from typing import BinaryIO

from aiobotocore.session import get_session
from dotenv import load_dotenv
from fastapi import UploadFile

load_dotenv()

ACCESS_KEY = environ.get("ACCESS_KEY")
SECRET_KEY = environ.get("SECRET_KEY")
ENDPOINT_URL = environ.get("ENDPOINT_URL")
BUCKET_NAME = environ.get("BUCKET_NAME")
STORAGE_URL = environ.get("STORAGE_URL")


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
            await client.delete_object(
                Bucket=self.bucket_name,
                Key=filename,
            )


async def upload_file(filename: str, file: UploadFile):
    s3_client = S3Client(
        access_key=f"{ACCESS_KEY}",
        secret_key=f"{SECRET_KEY}",
        endpoint_url=f"{ENDPOINT_URL}",
        bucket_name=f"{BUCKET_NAME}"
    )

    await s3_client.upload_file(filename=filename, file=file)
    return f"{STORAGE_URL}/{filename}"


async def upload_raw(filename: str, file: BinaryIO):
    s3_client = S3Client(
        access_key=f"{ACCESS_KEY}",
        secret_key=f"{SECRET_KEY}",
        endpoint_url=f"{ENDPOINT_URL}",
        bucket_name=f"{BUCKET_NAME}"
    )

    await s3_client.upload_raw(filename=filename, file=file)
    return f"{STORAGE_URL}/{filename}"


async def delete_file(filename: str):
    s3_client = S3Client(
        access_key=f"{ACCESS_KEY}",
        secret_key=f"{SECRET_KEY}",
        endpoint_url=f"{ENDPOINT_URL}",
        bucket_name=f"{BUCKET_NAME}"
    )

    await s3_client.delete_file(filename=filename)
