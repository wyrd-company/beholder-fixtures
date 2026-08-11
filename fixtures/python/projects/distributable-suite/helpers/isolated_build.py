"""PKG-002 isolated build demonstration.

PEP 517 isolated build with constrained backend absent from caller and supplied
offline from vendored wheelhouse; isolation stays enabled.

Build command (offline, isolation enabled):

    python -m pip wheel --no-index --find-links wheelhouse --wheel-dir dist distributions/suite_core

The build-system requires `setuptools==84.0.0` which is absent from the caller
environment and resolved from `wheelhouse/setuptools-84.0.0-py3-none-any.whl`
without downloads. `pip` creates an isolated build env per PEP 517.

Missing/unsatisfiable backend would fail; non-isolated escape (`--no-build-isolation`)
is not used.
"""

from __future__ import annotations

import pathlib
import subprocess
import sys

WHEELHOUSE = pathlib.Path(__file__).parents[1] / "wheelhouse"
BUILD_TARGET = pathlib.Path(__file__).parents[1] / "distributions" / "suite_core"


def build_offline_isolated() -> list[str]:
    cmd = [
        sys.executable,
        "-m",
        "pip",
        "wheel",
        "--no-index",
        "--find-links",
        str(WHEELHOUSE),
        "--wheel-dir",
        str(BUILD_TARGET.parent.parent / "dist"),
        str(BUILD_TARGET),
    ]
    return cmd


def self_hosting_note() -> str:
    return "self-hosting via backend-path not used; backend is vendored wheel"


def backend_path_note() -> str:
    return "backend-path would allow local backend without wheelhouse"
