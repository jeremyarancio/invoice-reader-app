# Parser feature development

The goal: train and deploy a custom ML model to parse invoices.

# Benchmark

We gathered 132 documents from:
- 31 personal invoices as freelancer
- 101 documents from HuggingFace datasets - [amaye15/invoices-google-ocr](https://huggingface.co/datasets/amaye15/invoices-google-ocr) - containing various template of invoices, scanned or code generated. 

Out of all these documents, only **47** are kept based on diversity and quality.

The document images are stored confidentially in AWS S3 for future evaluation.

## Evaluation

### Overall Metrics

| Metric | Gemini-2.5-Flash |
|--------|-------|
| Precision | 0.8356 |
| Recall | 0.8356 |
| F1 Score | 0.8356 |

### Gemini-2.5-Flash metrics per field

| Field Name | Precision | Recall | F1 Score |
|------------|-----------|--------|----------|
| currency | 0.9787 | 0.9787 | 0.9787 |
| gross_amount | 0.8298 | 0.8298 | 0.8298 |
| vat | 0.9362 | 0.9362 | 0.9362 |
| issued_date | 0.9362 | 0.9362 | 0.9362 |
| invoice_number | 1.0000 | 1.0000 | 1.0000 |
| client_name | 0.9574 | 0.9574 | 0.9574 |
| client_street_address_number | 0.9362 | 0.9362 | 0.9362 |
| client_street_address | 0.7447 | 0.7447 | 0.7447 |
| client_city | 0.9362 | 0.9362 | 0.9362 |
| client_zipcode | 0.4681 | 0.4681 | 0.4681 |
| client_country | 0.4681 | 0.4681 | 0.4681 |

# Notes

## Annotation with Label Studio

- Load with S3 instead of manual upload: allow image tracking (quite easy to setup)
- Using presigned-url, the file path is actually base64-encoded!
- Use Schema interfaces to validate incoming and outgoing data (from label studio, to dataset...)
## Evaluation

