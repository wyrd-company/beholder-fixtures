"""PKG-012 package data and installed resources helpers."""

from __future__ import annotations

import importlib.resources as res


def read_text_resource() -> str:
    return res.files("suite_core").joinpath("resources/data.txt").read_text(encoding="utf-8")


def read_binary_resource() -> bytes:
    return res.files("suite_core").joinpath("resources/binary.dat").read_bytes()


def demonstrate_archive_vs_installed() -> dict[str, str]:
    """Shows resource readable from installed form and via as_file for zip-archive."""
    text = read_text_resource()
    binary_len = len(read_binary_resource())
    with res.as_file(res.files("suite_core").joinpath("resources/data.txt")) as path:
        extracted = path.read_text(encoding="utf-8")
    return {"installed_text": text[:20], "binary_len": str(binary_len), "extracted_matches": str(extracted == text)}


def namespace_resource_note() -> str:
    return "namespace package suite_shared_ns resources aggregated via importlib.resources.files('suite_shared_ns')"

def editable_masks_omission_note() -> str:
    return "editable install exposes source tree directly; missing wheel data would be visible as missing resource"

def missing_wheel_note() -> str:
    return "source present but wheel missing resource would make read_text raise FileNotFoundError"
