import os
import tempfile
import pytest
from app.services.supabase_s3 import (
    DEFAULT_S3_BUCKET_NAME,
    DEFAULT_SUPABASE_PUBLIC_URL,
    get_s3_config,
    upload_video_to_supabase_s3,
)


def test_get_s3_config():
    cfg = get_s3_config()
    assert cfg["bucket_name"] == DEFAULT_S3_BUCKET_NAME
    assert cfg["public_url_base"] == DEFAULT_SUPABASE_PUBLIC_URL.rstrip("/")
    assert cfg["aws_access_key_id"] == "8c261e7e379bd12d8ede2984f8277a0a"


def test_upload_video_to_supabase_s3_success():
    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp:
        tmp.write(b"unit test mp4 content for supabase s3")
        temp_file_path = tmp.name

    try:
        res = upload_video_to_supabase_s3(temp_file_path)
        assert res["status"] == "success"
        assert res["bucket"] == DEFAULT_S3_BUCKET_NAME
        assert res["public_url"].startswith(DEFAULT_SUPABASE_PUBLIC_URL)
        assert res["file_size"] > 0
        assert "timestamp" in res
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)


def test_upload_video_file_not_found():
    with pytest.raises(FileNotFoundError):
        upload_video_to_supabase_s3("non_existent_video_file.mp4")
