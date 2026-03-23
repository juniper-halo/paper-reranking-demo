"""Sanity checks for fixed schema slots and default weights."""

from __future__ import annotations

from src.schema.fixed_schema import DEFAULT_SCHEMA_WEIGHTS, FIXED_SCHEMA_SLOTS, schema_validator


def test_fixed_schema_slots_match_expected_order() -> None:
    assert FIXED_SCHEMA_SLOTS == (
        "topic_match",
        "method_match",
        "relationship_match",
        "recency",
    )


def test_default_schema_weights_cover_all_slots() -> None:
    assert set(DEFAULT_SCHEMA_WEIGHTS.keys()) == set(FIXED_SCHEMA_SLOTS)
    assert abs(sum(DEFAULT_SCHEMA_WEIGHTS.values()) - 1.0) < 1e-9


def test_schema_validator_accepts_default_weights() -> None:
    assert schema_validator(DEFAULT_SCHEMA_WEIGHTS)


def test_schema_validator_rejects_missing_key() -> None:
    bad = dict(DEFAULT_SCHEMA_WEIGHTS)
    bad.pop("recency")
    assert not schema_validator(bad)


def test_schema_validator_rejects_bad_sum() -> None:
    bad = dict(DEFAULT_SCHEMA_WEIGHTS)
    bad["recency"] = 0.20
    assert not schema_validator(bad)
