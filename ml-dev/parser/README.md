# Parser feature development

The goal: train and deploy a custom ML model to parse invoices.

# Benchmark

We gathered 132 documents from:
- 31 personal invoices as freelancer
- 101 documents from HuggingFace datasets - [amaye15/invoices-google-ocr](https://huggingface.co/datasets/amaye15/invoices-google-ocr) - containing various template of invoices, scanned or code generated. 

The document images are stored confidentially in AWS S3 for future evaluation.

Scripts:
- `scripts/0_extract_pictures_from_dataset.py`
- `scripts/1_convert_pdf_to_image.sh`

# Notes

## Annotation with Label Studio

- Load with S3 instead of manual uplaod: allow image tracking (quite easy to setup)
- Using presigned-url, the file path is actually base64-encoded!
