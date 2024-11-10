import os
from typing import BinaryIO

from invoice_reader.core import storage
from invoice_reader.schemas import InvoiceMetadata

from dotenv import load_dotenv
load_dotenv()

def submit(user_id: str, file: BinaryIO, filename: str, metadata: InvoiceMetadata):
    file_format = os.path.splitext(filename)[-1]
    storage.store(user_id=user_id, file=file, file_format= file_format, metadata=metadata, bucket=os.getenv("BUCKET_NAME"))

def extract(file: BinaryIO) -> InvoiceMetadata:
    raise NotImplementedError
    
    
def get_user_id(token: str): 
    raise NotImplementedError
