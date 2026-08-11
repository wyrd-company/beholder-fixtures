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
    base = ["uv", "pip", "compile", "--no-index", "--find-links", "wheelhouse", "--find-links", "candidate_set"]
    return {
        "satisfiable": base + ["--offline", "-o", "satisfiable-lock.txt"] + SATISFIABLE_REQUIREMENTS,
        "conflict": base + ["--offline", "-o", "conflict-lock.txt"] + CONFLICT_REQUIREMENTS,
    }


def frontend_diagnostics_note() -> str:
    return "conflict branch yields 'No solution found' with reason: suite-core requires requests>=2.28.1 vs pinned 2.25.0"


def locked_sync_note() -> str:
    return "uv pip sync --offline applies locked satisfiable set into venv"
