import os
import tempfile
from app.services.publisher import (
    AUTHOR_NAME,
    AUTHOR_PROFILE_ID,
    PROFILE_URL,
    TARGET_FEED,
    publish_to_qoneqt,
)


def test_publish_to_qoneqt():
    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp:
        tmp.write(b"test video file content")
        temp_video_path = tmp.name

    try:
        title = "Test AI Short Video"
        result = publish_to_qoneqt(video_path=temp_video_path, title=title)

        assert result["status"] == "success"
        assert result["post_id"] == f"qlip_{AUTHOR_PROFILE_ID}_live"
        assert result["author"] == AUTHOR_NAME
        assert result["target"] == "Qlips Feed"
        assert result["profile_url"] == PROFILE_URL
    finally:
        if os.path.exists(temp_video_path):
            os.remove(temp_video_path)
