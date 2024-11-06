from typing import BinaryIO

from invoice_reader.core import storage
from invoice_reader.schemas import InvoiceMetadata


def submit(user_id: str, file: BinaryIO, metadata: InvoiceMetadata):
    storage.store(user_id=user_id, file=file, metadata=metadata)
    

def extract(file: BinaryIO) -> InvoiceMetadata:
    raise NotImplementedError
    
    
def get_user_id(token: str): 
    raise NotImplementedError
