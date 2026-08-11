"""PKG-019 dependency resolution with satisfiable branch and true conflict (offline)."""

from __future__ import annotations

import pathlib

# Offline local candidate set in candidate_set/
# candidates: suite_core 1.4.2 depends on requests>=2.28.1
# satisfiable branch: requests 2.31.0 satisfies >=2.28.1
# conflict branch: requests 2.25.0 does NOT satisfy >=2.28.1 but required by another dep

# Simulated candidate wheels (placeholders; resolution via uv offline):
# candidate_set/satisfiable/requests-2.31.0-py3-none-any.whl
# candidate_set/conflict/requests-2.25.0-py3-none-any.whl

SATISFIABLE_REQUIREMENTS = ["distributable-suite-core==1.4.2", "requests==2.31.0"]
CONFLICT_REQUIREMENTS = ["distributable-suite-core==1.4.2", "requests==2.25.0"]


def uv_resolution_commands() -> dict[str, list[str]]:
    base_satisfiable = [
        "uv", "pip", "compile",
        "--offline", "--no-index",
        "--find-links", "wheelhouse",
        "--find-links", "candidate_set/satisfiable",
        "--find-links", "dist",
    ]
    base_conflict = [
        "uv", "pip", "compile",
        "--offline", "--no-index",
        "--find-links", "wheelhouse",
        "--find-links", "candidate_set/conflict",
        "--find-links", "dist",
    ]
    return {
        "satisfiable": base_satisfiable + ["--output-file", "/tmp/satisfiable.txt", "candidate_set/requirements-satisfiable.txt"],
        "conflict": base_conflict + ["--output-file", "/tmp/conflict.txt", "candidate_set/requirements-conflict.txt"],
    }


def offline_satisfiable_demo() -> bool:
    """Run satisfiable branch offline via uv; expects exit 0."""
    import subprocess, pathlib
    root = pathlib.Path(__file__).parents[1]
    cmd = [
        "uv", "pip", "compile", "--offline", "--no-index",
        "--find-links", str(root / "wheelhouse"),
        "--find-links", str(root / "candidate_set" / "satisfiable"),
        "--find-links", str(root / "dist"),
        "--output-file", "/tmp/satisfiable.txt",
        str(root / "candidate_set" / "requirements-satisfiable.txt"),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0


def offline_conflict_demo() -> bool:
    """Run conflict branch offline; expects non-zero with diagnostics."""
    import subprocess, pathlib
    root = pathlib.Path(__file__).parents[1]
    cmd = [
        "uv", "pip", "compile", "--offline", "--no-index",
        "--find-links", str(root / "wheelhouse"),
        "--find-links", str(root / "candidate_set" / "conflict"),
        "--find-links", str(root / "dist"),
        "--output-file", "/tmp/conflict.txt",
        str(root / "candidate_set" / "requirements-conflict.txt"),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode != 0 and "No solution" in (result.stderr + result.stdout)


def frontend_diagnostics_note() -> str:
    return "conflict branch yields 'No solution found' with reason: suite-core requires requests>=2.28.1 vs pinned 2.25.0"


def locked_sync_note() -> str:
    return "uv pip sync --offline applies locked satisfiable set into venv"
