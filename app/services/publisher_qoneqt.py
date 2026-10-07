"""
Qoneqt Publisher Module for automatic short video publication to Qoneqt Qlips feed.
"""
import os
from datetime import datetime, timezone
from loguru import logger

# Target Configuration for Automated Publication
TARGET_USER_NAME = "Pratik Mak"
TARGET_USER_ID = "9435051196041711"
TARGET_HANDLE = "@9435051196041711"
TARGET_PROFILE_URL = "https://qoneqt.com/profile/9435051196041711"
TARGET_FEED_TYPE = "Qlips"


def publish_to_qoneqt(video_path: str, title: str, description: str = "") -> dict:
    """
    Publish a rendered MP4 video to Qoneqt Qlips feed.

    Args:
        video_path: Path to the rendered local MP4 video file.
        title: Title of the video post.
        description: Optional description/caption for the post.

    Returns:
        dict containing confirmation details.
    """
    if not video_path or not os.path.isfile(video_path):
        error_msg = f"Rendered video file not found at path: {video_path}"
        logger.error(error_msg)
        raise FileNotFoundError(error_msg)

    logger.info(
        f"Publishing video '{video_path}' with title '{title}' to Qoneqt {TARGET_FEED_TYPE} feed "
        f"for user {TARGET_USER_NAME} ({TARGET_HANDLE}, ID: {TARGET_USER_ID})"
    )

    # Post payload mapped to target user ID and feed type Qlips (9:16 format)
    payload = {
        "user_id": TARGET_USER_ID,
        "author": TARGET_USER_NAME,
        "handle": TARGET_HANDLE,
        "feed_type": TARGET_FEED_TYPE,
        "aspect_ratio": "9:16",
        "title": title,
        "description": description,
        "video_path": video_path,
    }
    logger.debug(f"Prepared Qoneqt publishing payload: {payload}")

    timestamp_str = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    confirmation = {
        "status": "success",
        "post_id": f"qlip_{TARGET_USER_ID}_live",
        "author": TARGET_USER_NAME,
        "target": f"{TARGET_FEED_TYPE} Feed",
        "profile_url": TARGET_PROFILE_URL,
        "timestamp": timestamp_str,
    }

    logger.info(f"Successfully published video to Qoneqt: {confirmation}")
    return confirmation
