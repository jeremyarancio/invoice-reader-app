import json
from parser.infrastructure.schemas.label_studio import LabelStudioExportJSONMIN


LABEL_STUDIO_EXPORT_PATH = "tests/data/label_studio_json_min_export.json"


def test_annotation_schema():
    with open(LABEL_STUDIO_EXPORT_PATH, "r") as f:
        items = json.load(f)
    for item in items:
        assert LabelStudioExportJSONMIN.model_validate(item)
