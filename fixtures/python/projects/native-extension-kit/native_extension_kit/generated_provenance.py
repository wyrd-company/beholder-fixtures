"""PY-CAN-NATIVE-006: freshness and provenance for generated modules."""

from __future__ import annotations

import hashlib
import json
import pathlib

INPUT = pathlib.Path(__file__).parent.parent / "generator_input" / "schema.json"


def check_freshness() -> dict[str, object]:
    raw = INPUT.read_bytes()
    current_hash = hashlib.sha256(raw).hexdigest()[:16]
    try:
        from .generated_models import __generated_hash__  # type: ignore[import-not-found]
    except Exception as exc:
        return {"fresh": False, "error": str(exc), "current_hash": current_hash}
    return {
        "fresh": current_hash == __generated_hash__,
        "current_hash": current_hash,
        "committed_hash": __generated_hash__,
        "provenance": "generator_input/schema.json retained input",
        "generator": "generate.py deterministic sorted output",
        "committed_vs_build_only": "committed output; build does not regenerate",
        "sdist_wheel_divergence": "sdist includes input + generated; wheel includes generated only",
        "missing_source_map": "no source map; provenance via SHA256 header",
    }


def provenance_info() -> dict[str, str]:
    return {
        "input": "generator_input/schema.json",
        "output_py": "native_extension_kit/generated_models.py",
        "output_pyi": "native_extension_kit/generated_models.pyi",
        "generator": "generate.py",
        "deterministic": "sorted models and fields, stable hash",
    }


__all__ = ["check_freshness", "provenance_info"]
