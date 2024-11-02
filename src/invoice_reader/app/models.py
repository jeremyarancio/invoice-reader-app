from pydantic import BaseModel

from fastapi import UploadFile

class UploadedFile(BaseModel):
    file: UploadFile


    