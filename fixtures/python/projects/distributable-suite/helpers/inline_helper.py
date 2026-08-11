"""PKG-021 inline script offline helper."""

from __future__ import annotations

import pathlib
import subprocess


def offline_inline_demo() -> bool:
    """Run inline_example.py offline via uv with local find-links."""
    root = pathlib.Path(__file__).parents[1]
    cmd = [
        "uv",
        "run",
        "--offline",
        "--find-links",
        str(root / "candidate_set" / "satisfiable"),
        "--find-links",
        str(root / "wheelhouse"),
        "--with",
        "requests",
        str(root / "scripts" / "inline_example.py"),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0 and "requests" in result.stdout
