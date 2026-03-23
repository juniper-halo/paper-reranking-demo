"""Wrapper around sentence-transformers model loading and embedding calls."""

from __future__ import annotations

from typing import Sequence

import numpy as np
import torch
from sentence_transformers import SentenceTransformer

from src import config


class TextEmbedder:
    """Lazy-loading embedder wrapper for sentence-transformers models."""

    def __init__(self, model_name: str = config.EMBEDDING_MODEL_NAME, device: str | None = None) -> None:
        """Initialize embedder state without immediately loading model weights."""
        self.model_name = model_name
        self.device = device or self._auto_device()
        self._model: SentenceTransformer | None = None

    def _auto_device(self) -> str:
        if torch.cuda.is_available():
            return "cuda"
        if torch.backends.mps.is_available():
            return "mps"
        return "cpu"

    def load_model(self) -> SentenceTransformer:
        """Load and cache the embedding model instance."""
        if self._model is None:
            self._model = SentenceTransformer(self.model_name, device=self.device)
        return self._model

    def encode(self, texts: Sequence[str]) -> np.ndarray:
        """Encode texts into dense vectors."""
        if not texts:
            return np.zeros((0, 0), dtype=float)

        model = self.load_model()
        embeddings = model.encode(list(texts), convert_to_numpy=True)
        return np.asarray(embeddings, dtype=float)
