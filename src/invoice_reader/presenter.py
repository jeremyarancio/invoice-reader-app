from io import BytesIO

from invoice_reader import settings

def upload(file: BytesIO):
    filepath = settings.SRC_DIR / "uploaded_file.pdf" 
    with filepath.open("wb") as f:
        f.write(file.read())
    return filepath