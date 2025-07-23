import base64
from io import BytesIO

from PIL.Image import Image
from transformers import AutoModel, AutoTokenizer, AutoProcessor

from ml_server.application.parser.interfaces import Parser
from ml_server.settings import settings


class NanonetsOCRParser(Parser):
    """Invoice Parser using Nanonets OCR: https://huggingface.co/nanonets/Nanonets-OCR-s."""

    def __init__(
        self, model: AutoModel, tokenizer: AutoTokenizer, processor: AutoProcessor
    ):
        self.model = model
        self.tokenizer = tokenizer
        self.processor = processor

        self.prompt = """Extract the following elements from the invoice image; """

    def parse(
        self, image: Image, max_new_tokens: int = settings.max_new_tokens
    ) -> dict:
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "url": f"data:image/png;base64,{img_str}"},
                    {
                        "type": "text",
                        "text": self.prompt,
                    },
                ],
            },
        ]
        text = self.processor.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        inputs = self.processor(
            text=[text], images=[image], padding=True, return_tensors="pt"
        )
        output_ids = self.model.generate(
            **inputs, max_new_tokens=max_new_tokens, do_sample=False
        )
        output_text = self.processor.batch_decode(
            output_ids, skip_special_tokens=True, clean_up_tokenization_spaces=True
        )
        return output_text[0]
