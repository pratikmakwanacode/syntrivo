import os
import tempfile
import pytest
from app.services.cloud_storage import (
    DEFAULT_S3_BUCKET_NAME,
    DEFAULT_SUPABASE_PUBLIC_URL,
    upload_video_to_cloud,
)
from app.services.task import _purge_local_task_files


def test_upload_video_to_cloud_success():
    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp:
        tmp.write(b"unit test video content for cloud storage")
        temp_path = tmp.name

    try:
        destination_name = "test_videos/unit_test_cloud.mp4"
        public_url = upload_video_to_cloud(temp_path, destination_name)

        assert public_url.startswith(DEFAULT_SUPABASE_PUBLIC_URL)
        assert destination_name in public_url
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


def test_upload_video_to_cloud_file_not_found():
    with pytest.raises(FileNotFoundError):
        upload_video_to_cloud("non_existent_file.mp4", "dest.mp4")


def test_purge_local_task_files():
    # Create temporary dummy files to simulate downloaded/compiled assets
    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as f1, \
         tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f2, \
         tempfile.NamedTemporaryFile(suffix=".srt", delete=False) as f3:
        f1.write(b"dummy final video")
        f2.write(b"dummy audio")
        f3.write(b"dummy subtitle")
        path1, path2, path3 = f1.name, f2.name, f3.name

    try:
        _purge_local_task_files(
            task_id="test_purge_task",
            local_final_video_paths=[path1],
            audio_file=path2,
            subtitle_path=path3,
        )

        assert not os.path.exists(path1)
        assert not os.path.exists(path2)
        assert not os.path.exists(path3)
    finally:
        for p in (path1, path2, path3):
            if os.path.exists(p):
                os.remove(p)
