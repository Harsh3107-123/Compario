from __future__ import annotations

from typing import List, Tuple

from PIL import Image
import numpy as np


# Keras MobileNetV2 kept for backward compatibility if needed elsewhere
try:
    from tensorflow.keras.applications.mobilenet_v2 import (
        MobileNetV2,
        preprocess_input as keras_preprocess_input,
        decode_predictions,
    )
except Exception:  # tensorflow may be optional now
    MobileNetV2 = None  # type: ignore
    keras_preprocess_input = None  # type: ignore
    decode_predictions = None  # type: ignore


_keras_model = None


def get_keras_mobilenet():
    global _keras_model
    if MobileNetV2 is None:
        raise RuntimeError("TensorFlow/Keras is not available")
    if _keras_model is None:
        _keras_model = MobileNetV2(weights="imagenet")
    return _keras_model


def classify_imagenet_topk(img_array: np.ndarray, top_k: int = 3) -> List[Tuple[str, str, float]]:
    if keras_preprocess_input is None or decode_predictions is None:
        raise RuntimeError("TensorFlow/Keras not available for classification")
    arr = keras_preprocess_input(img_array.copy())
    model = get_keras_mobilenet()
    preds = model.predict(arr, verbose=0)
    decoded = decode_predictions(preds, top=top_k)[0]
    return [(cid, label, float(prob)) for cid, label, prob in decoded]


def classify_with_hf(image: Image.Image, top_k: int = 3) -> List[Tuple[str, float]]:
    """Hugging Face ViT pipeline classification for a PIL image."""
    from transformers import pipeline

    clf = pipeline("image-classification", model="google/vit-base-patch16-224")
    rows = clf(image, top_k=top_k)
    return [(row.get("label", ""), float(row.get("score", 0.0))) for row in rows]


def classify_with_torchvision(image: Image.Image, top_k: int = 3) -> List[Tuple[str, float]]:
    """TorchVision ResNet-50 classification for a PIL image."""
    import torch
    from torchvision import models

    weights = models.ResNet50_Weights.IMAGENET1K_V2
    model = models.resnet50(weights=weights)
    model.eval()
    preprocess = weights.transforms()
    x = preprocess(image).unsqueeze(0)
    with torch.inference_mode():
        probs = torch.softmax(model(x), dim=1)[0]
        values, indices = probs.topk(top_k)
    categories = weights.meta.get("categories", [])
    output: List[Tuple[str, float]] = []
    for v, i in zip(values.tolist(), indices.tolist()):
        label = categories[i] if i < len(categories) else str(i)
        output.append((label, float(v)))
    return output


