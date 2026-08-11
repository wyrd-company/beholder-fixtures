# Generated from schema.json via generate.py — do not edit.
# Provenance: generator_input/schema.json SHA256:fc4993d3256d1ce6
# Generator: native-extension-kit 1.0.0
# Freshness: compare header SHA256 with current input hash via generated_provenance.check_freshness()
# sdist/wheel divergence: generated output is committed; build does not regenerate
# Stale output: rebuild with `task generate` when input changes

from __future__ import annotations

from dataclasses import dataclass

__generated_hash__ = "fc4993d3256d1ce6"
__generator_version__ = "1.0.0"

@dataclass
class SampleRecord:
    """Sample record generated from retained input."""
    active: bool
    label: str
    value: int

@dataclass
class TaggedItem:
    """Tagged item generated from retained input."""
    count: int
    tag: str

__all__ = [
    "SampleRecord",
    "TaggedItem",
    "__generated_hash__",
    "__generator_version__",
]
