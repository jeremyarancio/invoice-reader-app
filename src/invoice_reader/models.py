from dataclasses import dataclass


@dataclass
class S3:
    bucket: str
    suffix: str

    @property
    def path(self):
        return f"s3://{self.bucket}/{self.suffix}"
    
    @classmethod
    def init_from_id(cls, bucket: str, user_id: str, file_id: str) -> "S3":
        return cls(
            bucket=bucket,
            suffix=f"{user_id}/{file_id}"
        )
    
    def store(self):
        raise NotImplementedError