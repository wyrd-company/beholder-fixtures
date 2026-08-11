#!/usr/bin/env python3
"""Generate committed .py and .pyi for PY-CAN-NATIVE-006 from retained input."""

from __future__ import annotations

import hashlib
import json
import pathlib

ROOT = pathlib.Path(__file__).parent
INPUT = ROOT / "generator_input" / "schema.json"
OUT_PY = ROOT / "native_extension_kit" / "generated_models.py"
OUT_PYI = ROOT / "native_extension_kit" / "generated_models.pyi"

GENERATOR_VERSION = "1.0.0"


def _hash_input(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()[:16]


def main() -> None:
    raw = INPUT.read_bytes()
    payload = json.loads(raw.decode("utf-8"))
    input_hash = _hash_input(raw)
    models = sorted(payload.get("models", []), key=lambda m: m["name"])

    # --- generate .py ---
    lines: list[str] = []
    lines.append(f"# Generated from {INPUT.name} via generate.py — do not edit.")
    lines.append(f"# Provenance: generator_input/schema.json SHA256:{input_hash}")
    lines.append(f"# Generator: native-extension-kit {GENERATOR_VERSION}")
    lines.append("# Freshness: compare header SHA256 with current input hash via generated_provenance.check_freshness()")
    lines.append("# sdist/wheel divergence: generated output is committed; build does not regenerate")
    lines.append("# Stale output: rebuild with `task generate` when input changes")
    lines.append("")
    lines.append("from __future__ import annotations")
    lines.append("")
    lines.append("from dataclasses import dataclass")
    lines.append("")
    lines.append(f"__generated_hash__ = \"{input_hash}\"")
    lines.append(f"__generator_version__ = \"{GENERATOR_VERSION}\"")
    lines.append("")
    for model in models:
        name = model["name"]
        doc = model.get("doc", "")
        fields = model.get("fields", {})
        lines.append("@dataclass")
        lines.append(f"class {name}:")
        if doc:
            lines.append(f'    """{doc}"""')
        if not fields:
            lines.append("    pass")
        else:
            for field_name in sorted(fields):
                field_type = fields[field_name]
                lines.append(f"    {field_name}: {field_type}")
        lines.append("")

    lines.append("__all__ = [")
    for model in models:
        lines.append(f'    "{model["name"]}",')
    lines.append('    "__generated_hash__",')
    lines.append('    "__generator_version__",')
    lines.append("]")
    lines.append("")

    OUT_PY.write_text("\n".join(lines), encoding="utf-8")

    # --- generate .pyi ---
    pyi_lines: list[str] = []
    pyi_lines.append(f"# Generated from {INPUT.name} via generate.py — do not edit.")
    pyi_lines.append(f"# Provenance: generator_input/schema.json SHA256:{input_hash}")
    pyi_lines.append(f"# Generator: native-extension-kit {GENERATOR_VERSION}")
    pyi_lines.append("")
    pyi_lines.append("from dataclasses import dataclass")
    pyi_lines.append("")
    pyi_lines.append(f"__generated_hash__: str = \"{input_hash}\"")
    pyi_lines.append(f"__generator_version__: str = \"{GENERATOR_VERSION}\"")
    pyi_lines.append("")
    for model in models:
        name = model["name"]
        fields = model.get("fields", {})
        pyi_lines.append("@dataclass")
        pyi_lines.append(f"class {name}:")
        if not fields:
            pyi_lines.append("    pass")
        else:
            for field_name in sorted(fields):
                field_type = fields[field_name]
                pyi_lines.append(f"    {field_name}: {field_type}")
        pyi_lines.append("")
    pyi_lines.append("__all__: list[str]")
    pyi_lines.append("")

    OUT_PYI.write_text("\n".join(pyi_lines), encoding="utf-8")
    print(f"generated {OUT_PY} ({input_hash})")
    print(f"generated {OUT_PYI} ({input_hash})")


if __name__ == "__main__":
    main()
