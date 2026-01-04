from pathlib import Path
from tqdm import tqdm
from itertools import islice

from datasets import load_dataset, Dataset
from PIL.Image import Image

REPO_DIR = Path(__file__).parent.parent
DATA_DIR = REPO_DIR / "data"
DATASET_DIR = DATA_DIR / "dataset"
IMAGE_DIR = DATA_DIR / "documents/benchmark/hf"
IMAGE_FEATURE_NAME = "pixel_values"


def main():
    dataset = load_data_from_dir(DATASET_DIR, split="test")
    images = extract_images_from_dataset(dataset, image_feature_name=IMAGE_FEATURE_NAME)  # type: ignore
    for i, image in enumerate(images):
        image.save(IMAGE_DIR / f"invoice_hf_{i}.png")


def load_data_from_dir(data_dir: Path, split: str = "train"):
    dataset = load_dataset(str(data_dir), data_files=f"{split}-*")
    return dataset


def extract_images_from_dataset(
    dataset: Dataset, image_feature_name: str, limit: int = 100
) -> list[Image]:
    return [
        item[image_feature_name]
        for item in islice(tqdm(dataset.shuffle(seed=42)["train"], total=limit), limit)
    ]


if __name__ == "__main__":
    main()
