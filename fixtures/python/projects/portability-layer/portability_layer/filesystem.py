"""Filesystem encoding and path representations (PY-CAN-PLAT-001)."""

from __future__ import annotations

import os
import pathlib
import sys
from dataclasses import dataclass
from enum import Enum
from typing import Union

PathKind = Enum("PathKind", ["TEXT", "PATHLIB", "BYTES_GUARDED"])

PathInput = Union[str, os.PathLike[str], pathlib.Path]


def normalize_text_path(candidate: PathInput) -> pathlib.Path:
    """Normalize text or pathlib input to a pathlib.Path."""
    if isinstance(candidate, pathlib.Path):
        return candidate
    if isinstance(candidate, str):
        return pathlib.Path(candidate)
    return pathlib.Path(os.fspath(candidate))


def text_path_examples(base: pathlib.Path) -> dict[str, pathlib.Path]:
    """Return text-based and pathlib-based path representations."""
    text_joined = os.path.join(str(base), "reports", "summary.txt")
    pathlib_joined = base / "reports" / "summary.txt"
    resolved_text = pathlib.Path(text_joined).resolve()
    return {
        "text_joined": pathlib.Path(text_joined),
        "pathlib_joined": pathlib_joined,
        "resolved_text": resolved_text,
    }


def pathlib_variants(base: pathlib.Path) -> dict[str, object]:
    """Show pathlib pure versus concrete and string conversion variants."""
    pure = pathlib.PurePosixPath(str(base / "archive" / "item.txt"))
    concrete = base / "archive" / "item.txt"
    return {
        "pure": pure,
        "concrete": concrete,
        "as_posix": pure.as_posix(),
        "from_string": pathlib.Path(str(concrete)),
        "fspath": os.fspath(concrete),
    }


def guarded_bytes_name(tmpdir: pathlib.Path) -> dict[str, object]:
    """Return a guarded POSIX non-UTF-8 bytes name; safe on all platforms.

    Windows lane is excluded per brief: the bytes path is POSIX-only and
    guarded. All files still parse under the selected interpreter.
    """
    result: dict[str, object] = {"supported": False, "bytes_path": None, "text_surrogate": None}
    if os.name != "posix":
        return result
    # Use a bytes name with non-UTF-8 bytes \xff\xfe — valid only on POSIX.
    try:
        raw_bytes = os.path.join(os.fsencode(str(tmpdir)), b"asset_\xff\xfe.bin")
        # Demonstrate surrogateescape round-trip for unencodable bytes.
        text_via_surrogate = raw_bytes.decode("utf-8", errors="surrogateescape")
        roundtrip = text_via_surrogate.encode("utf-8", errors="surrogateescape")
        result.update(
            {
                "supported": True,
                "bytes_path": raw_bytes,
                "text_surrogate": text_via_surrogate,
                "roundtrip_ok": roundtrip == raw_bytes,
                "return_representation": type(os.fsdecode(raw_bytes)).__name__,
            }
        )
        # Optionally create and list via bytes API without requiring it for tests.
        try:
            with open(raw_bytes, "wb") as fh:
                fh.write(b"portability-layer probe")
            listed = os.listdir(os.fsencode(str(tmpdir)))
            result["listed_via_bytes"] = raw_bytes in [os.path.join(os.fsencode(str(tmpdir)), e) for e in listed]
        except OSError:
            pass
    except Exception:
        pass
    return result


def encoding_roundtrip(path: pathlib.Path) -> dict[str, object]:
    """Demonstrate explicit UTF-8, surrogateescape, and return representation."""
    sample = path / "sample.txt"
    sample.write_text("caf\u00e9 — na\u00efve", encoding="utf-8")
    text = sample.read_text(encoding="utf-8")
    raw = sample.read_bytes()
    decoded_strict = raw.decode("utf-8", errors="strict")
    decoded_surrogate = raw.decode("utf-8", errors="surrogateescape")
    return {
        "text": text,
        "raw_len": len(raw),
        "decoded_strict": decoded_strict,
        "decoded_surrogate": decoded_surrogate,
        "utf8_mode": sys.flags.utf8_mode,
    }


@dataclass(frozen=True)
class PathRecord:
    """Record associating a logical name with text and pathlib forms."""

    name: str
    text_path: str
    pathlib_path: pathlib.Path
    kind: PathKind = PathKind.TEXT

    def as_pathlib(self) -> pathlib.Path:
        return pathlib.Path(self.text_path) if self.kind == PathKind.TEXT else self.pathlib_path

    def exists_via_both(self) -> bool:
        p = self.as_pathlib()
        return os.path.exists(str(p)) and p.exists()


def resolve_portable_path(candidate: PathInput) -> pathlib.Path:
    """Resolve a portable path input to an absolute pathlib path."""
    return normalize_text_path(candidate).resolve()


def describe_filesystem_encoding() -> dict[str, object]:
    """Describe filesystem encoding relevant to path representations."""
    return {
        "filesystem_encoding": sys.getfilesystemencoding(),
        "filesystem_errors": sys.getfilesystemencodeerrors(),
        "utf8_mode": sys.flags.utf8_mode,
        "preferred_encoding": "utf-8",
    }
