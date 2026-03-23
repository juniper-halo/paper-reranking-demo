"""Definitions for the fixed four-slot reranking schema."""

from __future__ import annotations

from src.utils.logging_utils import setup_logger

logger = setup_logger(__name__)

FIXED_SCHEMA_SLOTS: tuple[str, str, str, str] = (
    "topic_match",
    "method_match",
    "relationship_match",
    "recency",
)

# topic_match: how closely a paper aligns with the topic/subdomain of interest.
# method_match: how well paper methods align with requested methodological cues.
# relationship_match: whether the paper captures the desired variable/concept relationship.
# recency: publication-year freshness normalized to [0, 1].
DEFAULT_SCHEMA_WEIGHTS: dict[str, float] = {
    "topic_match": 0.35,
    "method_match": 0.30,
    "relationship_match": 0.25,
    "recency": 0.10,
}

def schema_validator(schema: dict[str, float] | None, tolerance: float = 1e-9) -> bool:
    """Validate a schema weights mapping for the fixed four-slot schema.

    Validation rules:
    - schema must be a dict with exactly the fixed slot keys.
    - each weight must be numeric and non-negative.
    - weights must sum to 1.0 within a small tolerance.
    """
    if schema is None:
        logger.info("Invalid schema: schema is None.")
        return False

    expected_keys = set(FIXED_SCHEMA_SLOTS)
    actual_keys = set(schema.keys())

    missing = expected_keys - actual_keys
    extra = actual_keys - expected_keys
    if missing:
        logger.info("Invalid schema: missing keys: %s", sorted(missing))
        return False
    if extra:
        logger.info("Invalid schema: unexpected keys: %s", sorted(extra))
        return False

    weight_sum = 0.0
    for slot in FIXED_SCHEMA_SLOTS:
        value = schema[slot]
        if not isinstance(value, (int, float)):
            logger.info("Invalid schema: weight for '%s' is not numeric (%s).", slot, type(value).__name__)
            return False
        if value < 0.0:
            logger.info("Invalid schema: weight for '%s' is negative (%s).", slot, value)
            return False
        weight_sum += float(value)

    if abs(weight_sum - 1.0) > tolerance:
        logger.info("Invalid schema: weights sum to %.12f (expected 1.0).", weight_sum)
        return False

    return True
