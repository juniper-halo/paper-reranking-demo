"""Wrapper around sentence-transformers model loading and embedding calls."""

from __future__ import annotations

from typing import Sequence

import numpy as np
from sentence_transformers import SentenceTransformer

from src import config


class TextEmbedder:
    """Lazy-loading embedder wrapper for sentence-transformers models."""

    def __init__(self, model_name: str = config.EMBEDDING_MODEL_NAME) -> None:
        """Initialize embedder state without immediately loading model weights."""
        self.model_name = model_name
        self._model: SentenceTransformer | None = None

    def load_model(self) -> SentenceTransformer:
        """Load and cache the embedding model instance."""
        if self._model is None:
            # TODO: add device selection (cpu/cuda/mps) and reproducibility options.
            self._model = SentenceTransformer(self.model_name)
        return self._model

    def encode(self, texts: Sequence[str]) -> np.ndarray:
        """Encode texts into dense vectors.

        TODO: implement batching controls and embedding cache to reduce repeated work.
        """
        if not texts:
            return np.zeros((0, 0), dtype=float)

        model = self.load_model()
        embeddings = model.encode(list(texts), convert_to_numpy=True)
        return np.asarray(embeddings, dtype=float)
