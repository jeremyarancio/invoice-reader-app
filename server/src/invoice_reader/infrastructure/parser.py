from typing import BinaryIO

import httpx

from invoice_reader.domain.parser import ParserExtraction
from invoice_reader.services.exceptions import InfrastructureException
from invoice_reader.services.interfaces.parser import IParser
from invoice_reader.settings import get_settings

settings = get_settings()


class MLServerParser(IParser):
    def parse(self, file: BinaryIO) -> ParserExtraction:
        """Parse document using the /parser endpoint from the ML server."""
        files = {"upload_file": file}
        response = httpx.post(settings.parser_endpoint, files=files)
        if response.status_code != 200:
            raise InfrastructureException(
                message=f"""Failed to parse the invoice document.\n Error: {response.text}. 
                Response status: {response.status_code}""",
            )
        try:
            parsed_data = ParserExtraction.model_validate(response.json())
        except Exception as e:
            raise InfrastructureException(
                message="Failed to parse the invoice document. Error: " + str(e),
                status_code=422,
            ) from e
        return parsed_data
