"""
CareerEdge AI - Local Sentence Embedding Engine
Uses local ONNX quantized all-MiniLM-L6-v2 model with mean pooling & L2 normalization.
Runs 100% offline via QNN Execution Provider (on Snapdragon PCs) or CPUExecutionProvider.
"""

import os
import logging
from typing import List, Union, Tuple
import numpy as np
from tokenizers import Tokenizer

from backend.engine.qnn_runtime import get_runtime_manager

logger = logging.getLogger("careeredge.embeddings")

DEFAULT_MODEL_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "models",
    "all-MiniLM-L6-v2",
)


class LocalEmbeddingEngine:
    """
    Produces 384-dimensional dense semantic vectors using local ONNX model
    accelerated by Qualcomm QNN (NPU) or CPU fallback.
    """

    def __init__(self, model_dir: str = DEFAULT_MODEL_DIR):
        self.model_dir = model_dir
        self.tokenizer_path = os.path.join(model_dir, "tokenizer.json")
        self.runtime_mgr = get_runtime_manager()

        if os.path.exists(self.tokenizer_path):
            self.tokenizer = Tokenizer.from_file(self.tokenizer_path)
            self.tokenizer.enable_truncation(max_length=128)
            self.tokenizer.enable_padding(length=128)
            logger.info("Local tokenizer loaded successfully.")
        else:
            self.tokenizer = None
            logger.warning(f"Tokenizer file not found at: {self.tokenizer_path}")

    def encode(
        self, texts: Union[str, List[str]], batch_size: int = 16
    ) -> Tuple[np.ndarray, float]:
        """
        Encodes one or multiple strings into normalized 384-dimensional dense vectors.
        Returns: (embeddings array of shape (N, 384), total_latency_ms)
        """
        if isinstance(texts, str):
            texts = [texts]

        if not texts:
            return np.empty((0, 384), dtype=np.float32), 0.0

        if not self.tokenizer or not self.runtime_mgr.session:
            # Fallback embedding if model is absent
            return self._fallback_embedding(texts)

        total_latency = 0.0
        all_embeddings = []

        # Process in batches
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i : i + batch_size]
            encodings = self.tokenizer.encode_batch(batch_texts)

            input_ids = np.array([e.ids for e in encodings], dtype=np.int64)
            attention_mask = np.array([e.attention_mask for e in encodings], dtype=np.int64)
            token_type_ids = np.array([e.type_ids for e in encodings], dtype=np.int64)

            feed_dict = {
                "input_ids": input_ids,
                "attention_mask": attention_mask,
            }
            # Add token_type_ids only if expected by model
            input_names = [inp.name for inp in self.runtime_mgr.session.get_inputs()]
            if "token_type_ids" in input_names:
                feed_dict["token_type_ids"] = token_type_ids

            outputs, lat_ms = self.runtime_mgr.run_inference(feed_dict)
            total_latency += lat_ms

            # Mean pooling over valid attention tokens
            last_hidden_state = outputs[0]  # shape: (B, seq_len, 384)
            input_mask_expanded = np.expand_dims(attention_mask, -1).astype(np.float32)

            sum_embeddings = np.sum(last_hidden_state * input_mask_expanded, axis=1)
            sum_mask = np.clip(input_mask_expanded.sum(axis=1), a_min=1e-9, a_max=None)
            mean_pooled = sum_embeddings / sum_mask

            # L2 normalize
            norms = np.linalg.norm(mean_pooled, axis=1, keepdims=True)
            norms = np.clip(norms, a_min=1e-9, a_max=None)
            normalized = mean_pooled / norms

            all_embeddings.append(normalized.astype(np.float32))

        final_embeddings = np.vstack(all_embeddings)
        return final_embeddings, round(total_latency, 2)

    def compute_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """
        Computes cosine similarity between two normalized vectors. Range: [-1.0, 1.0].
        Clamped to [0.0, 1.0] for career matching.
        """
        dot = float(np.dot(vec1.flatten(), vec2.flatten()))
        return max(0.0, min(1.0, (dot + 1.0) / 2.0))

    def _fallback_embedding(self, texts: List[str]) -> Tuple[np.ndarray, float]:
        """
        Deterministic hash-based vector generator in case ONNX model is uninitialized.
        """
        import hashlib
        vectors = []
        for text in texts:
            vec = np.zeros(384, dtype=np.float32)
            words = text.lower().split()
            for idx, word in enumerate(words):
                h = int(hashlib.md5(word.encode()).hexdigest(), 16)
                pos = h % 384
                vec[pos] += 1.0 / (idx + 1)
            norm = np.linalg.norm(vec)
            if norm > 0:
                vec = vec / norm
            vectors.append(vec)
        return np.vstack(vectors), 0.5


# Singleton embedding engine instance
_embedding_engine: Union[LocalEmbeddingEngine, None] = None


def get_embedding_engine() -> LocalEmbeddingEngine:
    global _embedding_engine
    if _embedding_engine is None:
        _embedding_engine = LocalEmbeddingEngine()
    return _embedding_engine
