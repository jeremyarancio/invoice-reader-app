"""Utils for S3"""

import uuid


def get_suffix_from_s3_path(s3_path: str) -> str:
    return "/".join(s3_path.split("://")[-1].split("/")[1:])


def get_s3_path(bucket: str, suffix: str) -> str:
    return f"s3://{bucket}/{suffix}"


def get_s3_suffix_from_data(
    user_id: uuid.UUID, file_id: uuid.UUID, file_format: str
) -> str:
    return f"{user_id}/{file_id}{file_format}"
