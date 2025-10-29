from parser.infrastructure.storage import S3StorageRepository
from parser.service.ports.storage import IStorageRepository
from parser.settings import get_settings

settings = get_settings()


def get_storage_repository() -> IStorageRepository:
    return S3StorageRepository()
