import os
import tempfile
import pytest
from app.services.publisher_qoneqt import (
    TARGET_FEED_TYPE,
    TARGET_HANDLE,
    TARGET_PROFILE_URL,
    TARGET_USER_ID,
    TARGET_USER_NAME,
    publish_to_qoneqt,
)


def test_publish_to_qoneqt_success():
    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp:
        tmp.write(b"fake video data")
        temp_video_path = tmp.name

    try:
        title = "Test AI Short Video"
        description = "Automated test description"

        result = publish_to_qoneqt(video_path=temp_video_path, title=title, description=description)

        assert result["status"] == "success"
        assert result["post_id"] == f"qlip_{TARGET_USER_ID}_live"
        assert result["author"] == TARGET_USER_NAME
        assert result["target"] == f"{TARGET_FEED_TYPE} Feed"
        assert result["profile_url"] == TARGET_PROFILE_URL
        assert "timestamp" in result
    finally:
        if os.path.exists(temp_video_path):
            os.remove(temp_video_path)


def test_publish_to_qoneqt_file_not_found():
    with pytest.raises(FileNotFoundError):
        publish_to_qoneqt(video_path="non_existent_file.mp4", title="Test Title")
