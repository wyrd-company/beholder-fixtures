"""Text encoding, newline and locale handling (PY-CAN-PLAT-004)."""

from __future__ import annotations

import io
import locale
import os
import pathlib
import subprocess
import sys
import tempfile
from dataclasses import dataclass


@dataclass(frozen=True)
class EncodingResult:
    path: pathlib.Path
    encoding: str
    newline: str | None
    text: str


def write_explicit_utf8(path: pathlib.Path, text: str) -> EncodingResult:
    """Write with explicit UTF-8 and read back to confirm round-trip."""
    path.write_text(text, encoding="utf-8", newline="\n")
    observed = path.read_text(encoding="utf-8")
    assert observed == text
    return EncodingResult(path=path, encoding="utf-8", newline="\n", text=observed)


def read_with_explicit_utf8(path: pathlib.Path) -> str:
    """Read with explicit UTF-8 encoding."""
    with path.open("r", encoding="utf-8", errors="strict") as fh:
        return fh.read()


def read_with_universal_newlines(path: pathlib.Path) -> list[str]:
    """Read using universal newline mode (newline=None)."""
    # universal mode translates \r, \n, \r\n to \n on input
    with path.open("r", encoding="utf-8", newline=None) as fh:
        content = fh.read()
    # Also demonstrate via io.open
    with io.open(str(path), "r", encoding="utf-8", newline=None) as fh2:
        _ = fh2.read()
    return content.splitlines()


def write_mixed_newlines(path: pathlib.Path) -> pathlib.Path:
    """Write a file with mixed newlines for universal-newline input demonstration."""
    # Use newline="" + binary write to preserve exact sequences
    path.write_bytes(b"line one\r\nline two\nline three\rlast")
    return path


def read_preserving_newlines(path: pathlib.Path) -> str:
    """Read with newline='' to preserve original newline sequences."""
    with path.open("r", encoding="utf-8", newline="") as fh:
        return fh.read()


@dataclass(frozen=True)
class LocaleProbe:
    locale_name: str | None
    encoding: str
    utf8_mode: int


def probe_locale_settings() -> LocaleProbe:
    return LocaleProbe(
        locale_name=locale.getlocale()[0],
        encoding=locale.getpreferredencoding(False),
        utf8_mode=sys.flags.utf8_mode,
    )


def spawn_with_utf8_mode(code: str, utf8_mode: int) -> subprocess.CompletedProcess[str]:
    """Spawn a child interpreter with PYTHONUTF8 varying (declared child-process context)."""
    env = os.environ.copy()
    env["PYTHONUTF8"] = str(utf8_mode)
    return subprocess.run(
        [sys.executable, "-c", code],
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )


def spawn_with_locale(code: str, locale_value: str) -> subprocess.CompletedProcess[str]:
    """Spawn a child with explicit locale-related env (LC_ALL / LANG)."""
    env = os.environ.copy()
    env["LC_ALL"] = locale_value
    env["LANG"] = locale_value
    # Keep PYTHONUTF8 explicit so locale vs UTF-8 mode interaction is observable.
    return subprocess.run(
        [sys.executable, "-c", code],
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )


def subprocess_locale_and_utf8_variants() -> dict[str, object]:
    """Run subprocess locale and UTF-8-mode variants (PY-CAN-PLAT-004)."""
    code_utf8 = "import sys; print(sys.flags.utf8_mode); print(sys.getfilesystemencoding())"
    r_default = spawn_with_utf8_mode(code_utf8, 0)
    r_utf8 = spawn_with_utf8_mode(code_utf8, 1)
    code_locale = "import locale; print(locale.getpreferredencoding(False)); print(locale.getlocale())"
    r_c_locale = spawn_with_locale(code_locale, "C")
    # Universal newline subprocess: feed mixed newlines via stdin bytes and read.
    mixed = b"a\r\nb\nc\rd"
    proc = subprocess.run(
        [sys.executable, "-c", "import sys; data=sys.stdin.read(); print(repr(data))"],
        input=mixed.decode("utf-8", errors="surrogateescape"),
        capture_output=True,
        text=True,
        check=False,
    )
    return {
        "utf8_default": {"stdout": r_default.stdout.strip(), "returncode": r_default.returncode},
        "utf8_enabled": {"stdout": r_utf8.stdout.strip(), "returncode": r_utf8.returncode},
        "c_locale": {"stdout": r_c_locale.stdout.strip(), "returncode": r_c_locale.returncode},
        "universal_input": proc.stdout.strip(),
    }


def demonstrate_text_variants() -> dict[str, object]:
    with tempfile.TemporaryDirectory() as td:
        base = pathlib.Path(td)
        mixed = write_mixed_newlines(base / "mixed.txt")
        universal_lines = read_with_universal_newlines(mixed)
        preserved = read_preserving_newlines(mixed)
        explicit = write_explicit_utf8(base / "explicit.txt", "caf\u00e9 — \u2603")
        return {
            "universal_lines": universal_lines,
            "preserved_raw": repr(preserved),
            "explicit": explicit,
            "locale_probe": probe_locale_settings(),
            "subprocess_variants": subprocess_locale_and_utf8_variants(),
        }
