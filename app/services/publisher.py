"""
Qoneqt publishing service module wrapper.
"""
from app.services.publisher_qoneqt import (
    TARGET_FEED_TYPE,
    TARGET_HANDLE,
    TARGET_PROFILE_URL,
    TARGET_USER_ID,
    TARGET_USER_NAME,
    publish_to_qoneqt,
)

AUTHOR_PROFILE_ID = TARGET_USER_ID
AUTHOR_NAME = TARGET_USER_NAME
PROFILE_URL = TARGET_PROFILE_URL
TARGET_FEED = f"Qoneqt {TARGET_FEED_TYPE} Feed"

__all__ = [
    "publish_to_qoneqt",
    "TARGET_USER_NAME",
    "TARGET_USER_ID",
    "TARGET_HANDLE",
    "TARGET_PROFILE_URL",
    "TARGET_FEED_TYPE",
    "AUTHOR_PROFILE_ID",
    "AUTHOR_NAME",
    "PROFILE_URL",
    "TARGET_FEED",
]
