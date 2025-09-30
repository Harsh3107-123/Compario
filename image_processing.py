from __future__ import annotations

import io
from typing import Tuple

import cv2
import numpy as np
from PIL import Image
from tensorflow.keras.preprocessing import image as keras_image


def preprocess_image_for_classification(
    uploaded_file: io.BytesIO,
    target_size: Tuple[int, int] = (224, 224),
):
    """Preprocess an uploaded image for CNN classification.

    Steps:
    - Read PIL RGB image
    - Denoise with fastNlMeansDenoisingColored
    - Resize to target_size
    - Return (model_input_array, display_image)
    """
    pil_img = Image.open(uploaded_file).convert("RGB")
    cv_img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    denoised = cv2.fastNlMeansDenoisingColored(cv_img, None, 5, 5, 7, 21)
    resized = cv2.resize(denoised, target_size, interpolation=cv2.INTER_AREA)
    rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
    disp_img = Image.fromarray(rgb)

    img_array = keras_image.img_to_array(disp_img)
    img_array = np.expand_dims(img_array, axis=0)
    return img_array, disp_img


def is_within_size_limit(uploaded_file: io.BytesIO, max_mb: float = 5.0) -> bool:
    """Return True if file size is within limit in MB."""
    size_attr = getattr(uploaded_file, "size", None)
    if size_attr is None:
        return True
    return (size_attr / (1024 * 1024)) <= max_mb


def load_pil_rgb(uploaded_file: io.BytesIO) -> Image.Image:
    """Load an uploaded file as a PIL RGB image."""
    return Image.open(uploaded_file).convert("RGB")


