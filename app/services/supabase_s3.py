"""
Supabase S3 Storage Service (Syntrivo)
Uploads generated videos to Supabase S3 bucket and provides public URLs.
"""
import mimetypes
import os
from datetime import datetime, timezone
import boto3
from botocore.exceptions import BotoCoreError, ClientError
from loguru import logger
from app.config import config

# Default configuration fallbacks for Syntrivo S3
DEFAULT_S3_ENDPOINT_URL = "https://lszwauiynaiszwhwwjtd.storage.supabase.co/storage/v1/s3"
DEFAULT_S3_REGION = "ap-northeast-2"
DEFAULT_S3_BUCKET_NAME = "syntrivo-videos"
DEFAULT_SUPABASE_PUBLIC_URL = "https://lszwauiynaiszwhwwjtd.supabase.co/storage/v1/object/public/syntrivo-videos"
DEFAULT_S3_ACCESS_KEY_ID = "8c261e7e379bd12d8ede2984f8277a0a"
DEFAULT_S3_SECRET_ACCESS_KEY = "3f48bdf0e0635f00b90597579813f07de85b1f2b638e9e08ad4c1031e6b94b72"


def get_s3_config() -> dict:
    """Read S3 config from environment variables or config.toml [s3] section."""
    s3_section = getattr(config, "s3", {}) if hasattr(config, "s3") else {}
    if not isinstance(s3_section, dict):
        s3_section = {}

    endpoint_url = os.getenv("S3_ENDPOINT_URL", s3_section.get("endpoint_url") or DEFAULT_S3_ENDPOINT_URL)
    region = os.getenv("S3_REGION", s3_section.get("region") or DEFAULT_S3_REGION)
    bucket_name = os.getenv("S3_BUCKET_NAME", s3_section.get("bucket_name") or DEFAULT_S3_BUCKET_NAME)
    public_url_base = os.getenv("SUPABASE_PUBLIC_URL", s3_section.get("public_url") or DEFAULT_SUPABASE_PUBLIC_URL).rstrip("/")
    access_key_id = os.getenv("S3_ACCESS_KEY_ID", s3_section.get("access_key_id") or DEFAULT_S3_ACCESS_KEY_ID)
    secret_access_key = os.getenv("S3_SECRET_ACCESS_KEY", s3_section.get("secret_access_key") or DEFAULT_S3_SECRET_ACCESS_KEY)

    return {
        "endpoint_url": endpoint_url,
        "region_name": region,
        "bucket_name": bucket_name,
        "public_url_base": public_url_base,
        "aws_access_key_id": access_key_id,
        "aws_secret_access_key": secret_access_key,
    }


def get_s3_client():
    """Create and return a boto3 S3 client for Supabase S3."""
    cfg = get_s3_config()
    return boto3.client(
        "s3",
        endpoint_url=cfg["endpoint_url"],
        region_name=cfg["region_name"],
        aws_access_key_id=cfg["aws_access_key_id"],
        aws_secret_access_key=cfg["aws_secret_access_key"],
    )


def upload_video_to_supabase_s3(file_path: str, object_key: str | None = None) -> dict:
    """
    Upload a local video file to Supabase S3 bucket (syntrivo-videos).

    Args:
        file_path: Path to local video file.
        object_key: Optional S3 key destination. If omitted, generates a unique key.

    Returns:
        dict containing status, bucket, object_key, public_url, and file metadata.
    """
    if not file_path or not os.path.isfile(file_path):
        error_msg = f"Video file not found for S3 upload: {file_path}"
        logger.error(error_msg)
        raise FileNotFoundError(error_msg)

    cfg = get_s3_config()
    filename = os.path.basename(file_path)
    if not object_key:
        timestamp_prefix = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        object_key = f"videos/{timestamp_prefix}_{filename}"

    mime_type = mimetypes.guess_type(file_path)[0] or "video/mp4"
    file_size = os.path.getsize(file_path)

    logger.info(
        f"Uploading '{file_path}' ({file_size} bytes) to Supabase S3 bucket "
        f"'{cfg['bucket_name']}' as key '{object_key}'"
    )

    client = get_s3_client()
    try:
        with open(file_path, "rb") as body:
            client.put_object(
                Bucket=cfg["bucket_name"],
                Key=object_key,
                Body=body,
                ContentType=mime_type,
            )

        public_url = f"{cfg['public_url_base']}/{object_key}"
        timestamp_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        result = {
            "status": "success",
            "bucket": cfg["bucket_name"],
            "object_key": object_key,
            "public_url": public_url,
            "file_name": filename,
            "file_size": file_size,
            "content_type": mime_type,
            "timestamp": timestamp_iso,
        }

        logger.info(f"Successfully uploaded to Supabase S3: {result['public_url']}")
        return result

    except (BotoCoreError, ClientError) as exc:
        logger.exception(f"Failed to upload to Supabase S3: {exc}")
        raise RuntimeError(f"Supabase S3 upload failed: {exc}") from exc
