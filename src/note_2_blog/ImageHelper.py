from typing import List
import random
from pathlib import Path
from loguru import logger


class ImageManager:
    def __init__(self, image_path: str) -> None:
        self.images: List[str] = []
        self.used_images: List[str] = []
        logger.info(f"read image from {image_path}")
        self._read_image_paths(image_path)

    def _read_image_paths(self, path: str) -> List[str]:
        image_extensions = [".jpg", ".png", ".jpeg"]
        for ext in image_extensions:
            for file_path in Path(path).rglob(f"*{ext}"):
                self.images.append(str(file_path))
        return self.images

    def getImage(self) -> str:
        if len(self.used_images) == len(self.images):
            logger.error("All the images have been used up")
            raise Exception("All the images have been used up")
        image = random.choice(self.images)
        while True:
            if image not in self.used_images:
                self.used_images.append(image)
                logger.info(f"use image {image}")
                return image
            image = random.choice(self.images)
