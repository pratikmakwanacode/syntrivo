"""
Production Cloud Storage Service (Supabase S3)
Handles cloud video uploads and public streaming URL generation.
"""
import mimetypes
import os
import boto3
from botocore.exceptions import BotoCoreError, ClientError
from loguru import logger

# Default Syntrivo Supabase S3 credentials fallback if env is omitted
DEFAULT_S3_ENDPOINT_URL = "https://lszwauiynaiszwhwwjtd.storage.supabase.co/storage/v1/s3"
DEFAULT_S3_REGION = "ap-northeast-2"
DEFAULT_S3_BUCKET_NAME = "syntrivo-videos"
DEFAULT_SUPABASE_PUBLIC_URL = "https://lszwauiynaiszwhwwjtd.supabase.co/storage/v1/object/public/syntrivo-videos"
DEFAULT_S3_ACCESS_KEY_ID = "8c261e7e379bd12d8ede2984f8277a0a"
DEFAULT_S3_SECRET_ACCESS_KEY = "3f48bdf0e0635f00b90597579813f07de85b1f2b638e9e08ad4c1031e6b94b72"


def get_s3_client():
    endpoint_url = os.getenv("S3_ENDPOINT_URL") or DEFAULT_S3_ENDPOINT_URL
    aws_access_key_id = os.getenv("S3_ACCESS_KEY_ID") or DEFAULT_S3_ACCESS_KEY_ID
    aws_secret_access_key = os.getenv("S3_SECRET_ACCESS_KEY") or DEFAULT_S3_SECRET_ACCESS_KEY
    region_name = os.getenv("S3_REGION", DEFAULT_S3_REGION)

    return boto3.client(
        "s3",
        endpoint_url=endpoint_url,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name,
    )


def upload_video_to_cloud(local_file_path: str, destination_name: str) -> str:
    """
    Upload local video file to S3_BUCKET_NAME ("syntrivo-videos") with ExtraArgs={'ContentType': 'video/mp4'}.
    Returns public streaming URL.
    """
    if not local_file_path or not os.path.isfile(local_file_path):
        raise FileNotFoundError(f"Local file not found for cloud upload: {local_file_path}")

    bucket_name = os.getenv("S3_BUCKET_NAME") or DEFAULT_S3_BUCKET_NAME
    public_url_base = (os.getenv("SUPABASE_PUBLIC_URL") or DEFAULT_SUPABASE_PUBLIC_URL).rstrip("/")

    mime_type = mimetypes.guess_type(local_file_path)[0] or "video/mp4"

    logger.info(
        f"Uploading '{local_file_path}' to S3 bucket '{bucket_name}' "
        f"as '{destination_name}' with ContentType='{mime_type}'"
    )

    client = get_s3_client()
    try:
        client.upload_file(
            Filename=local_file_path,
            Bucket=bucket_name,
            Key=destination_name,
            ExtraArgs={"ContentType": mime_type},
        )

        public_url = f"{public_url_base}/{destination_name.lstrip('/')}"
        logger.info(f"Cloud upload successful. Public URL: {public_url}")
        return public_url
    except (BotoCoreError, ClientError) as exc:
        logger.exception(f"Cloud storage upload failed: {exc}")
        raise RuntimeError(f"Cloud storage upload failed: {exc}") from exc
