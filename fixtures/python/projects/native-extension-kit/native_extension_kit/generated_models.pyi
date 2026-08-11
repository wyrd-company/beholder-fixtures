# Generated from schema.json via generate.py — do not edit.
# Provenance: generator_input/schema.json SHA256:fc4993d3256d1ce6
# Generator: native-extension-kit 1.0.0

from dataclasses import dataclass

__generated_hash__: str = "fc4993d3256d1ce6"
__generator_version__: str = "1.0.0"

@dataclass
class SampleRecord:
    active: bool
    label: str
    value: int

@dataclass
class TaggedItem:
    count: int
    tag: str

__all__: list[str]
