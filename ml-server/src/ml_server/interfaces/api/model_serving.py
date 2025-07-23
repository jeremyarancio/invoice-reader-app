from io import BytesIO

from PIL import Image
from transformers import AutoProcessor, AutoTokenizer, AutoModelForImageTextToText
import litserve as ls

from ml_server.settings import settings
from ml_server.application.parser.service import ParserService
from ml_server.interfaces.dependencies.parser import get_parser


class HuggingFaceLitAPI(ls.LitAPI):
    def setup(self, device):
        model_name = settings.model_name

        self.model = AutoModelForImageTextToText.from_pretrained(
            model_name,
            torch_dtype="auto",
            device_map="auto",
            load_in_4bit=True,
        )
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.processor = AutoProcessor.from_pretrained(model_name)

    def decode_request(self, request):
        image_bytes = bytes.fromhex(request["image_bytes"])
        image = Image.open(BytesIO(image_bytes))
        return image

    def predict(self, image):
        parser = get_parser(
            model=self.model,
            tokenizer=self.tokenizer,
            processor=self.processor,
        )
        output = ParserService(parser=parser).parse(image=image)
        return output

    def encode_response(self, output):
        return {"output": output}


if __name__ == "__main__":
    api = HuggingFaceLitAPI()
    server = ls.LitServer(api, accelerator="auto", devices=4, workers_per_device=2)
    server.run(port=8000)
