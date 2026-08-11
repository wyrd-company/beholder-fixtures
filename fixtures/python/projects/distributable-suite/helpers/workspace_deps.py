"""PKG-020 multi-distribution workspace and local dependencies, resolved offline.

``suite_workspace_beta`` depends on ``suite_workspace_alpha``, bound to the
sibling workspace member via ``[tool.uv.sources] suite-workspace-alpha =
{workspace = true}`` in the workspace root. Three offline paths are executed:

- development: an editable install of both members, where beta imports alpha;
- published: both members built to a wheel directory offline, then beta
  installed from that directory so it pulls alpha by name;
- uv workspace: ``uv sync --offline`` resolving the workspace from the vendored
  wheelhouse.

All builds resolve the pinned setuptools backend from the vendored wheelhouse
with no network access.
"""

from __future__ import annotations

import os
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).parents[1]
WHEELHOUSE = ROOT / "wheelhouse"
WORKSPACE = ROOT / "workspace"
ALPHA = WORKSPACE / "suite_workspace_alpha"
BETA = WORKSPACE / "suite_workspace_beta"
_BIN = "Scripts" if sys.platform == "win32" else "bin"

# A neutral cwd keeps the current directory from being importable as an empty
# PEP 420 namespace package and masking a real import failure.
_NEUTRAL_CWD = tempfile.gettempdir()


def development_editable_offline() -> bool:
    """Editable install of both members offline; beta imports alpha."""
    with tempfile.TemporaryDirectory() as td:
        venv = pathlib.Path(td) / "venv"
        subprocess.run([sys.executable, "-m", "venv", str(venv)], check=True)
        py = venv / _BIN / "python"
        install = subprocess.run(
            [str(py), "-m", "pip", "install", "--no-index", "--find-links", str(WHEELHOUSE),
             "--no-deps", "-e", str(ALPHA), "-e", str(BETA)],
            capture_output=True, text=True,
        )
        if install.returncode != 0:
            return False
        check = subprocess.run(
            [str(py), "-c", "import suite_workspace_beta, suite_workspace_alpha; print('ok')"],
            capture_output=True, text=True, cwd=_NEUTRAL_CWD,
        )
        return check.returncode == 0 and "ok" in check.stdout


def published_resolution_offline() -> bool:
    """Build both members to a wheel dir offline, then install beta so it pulls alpha."""
    with tempfile.TemporaryDirectory() as td:
        dist = pathlib.Path(td) / "dist"
        build = subprocess.run(
            [sys.executable, "-m", "pip", "wheel", "--no-index", "--find-links", str(WHEELHOUSE),
             "--no-deps", "--wheel-dir", str(dist), str(ALPHA), str(BETA)],
            capture_output=True, text=True,
        )
        if build.returncode != 0:
            return False
        venv = pathlib.Path(td) / "venv"
        subprocess.run([sys.executable, "-m", "venv", str(venv)], check=True)
        py = venv / _BIN / "python"
        install = subprocess.run(
            [str(py), "-m", "pip", "install", "--no-index", "--find-links", str(dist),
             "--find-links", str(WHEELHOUSE), "suite-workspace-beta"],
            capture_output=True, text=True,
        )
        if install.returncode != 0:
            return False
        check = subprocess.run(
            [str(py), "-c", "import suite_workspace_beta, suite_workspace_alpha; print('ok')"],
            capture_output=True, text=True, cwd=_NEUTRAL_CWD,
        )
        return check.returncode == 0 and "ok" in check.stdout


def uv_workspace_sync_offline() -> bool:
    """uv resolves the workspace offline from the vendored wheelhouse.

    The workspace is copied to a temp directory first so the generated
    ``uv.lock`` and ``.venv`` never touch tracked source.
    """
    import shutil
    with tempfile.TemporaryDirectory() as td:
        work = pathlib.Path(td) / "workspace"
        shutil.copytree(WORKSPACE, work, ignore=shutil.ignore_patterns(".venv", "uv.lock", "*.egg-info", "build", "dist"))
        env = os.environ.copy()
        env["UV_CACHE_DIR"] = str(pathlib.Path(td) / "cache")
        result = subprocess.run(
            ["uv", "sync", "--offline", "--no-index", "--find-links", str(WHEELHOUSE)],
            cwd=str(work), env=env, capture_output=True, text=True,
        )
        return result.returncode == 0


def demonstrate() -> dict[str, bool]:
    return {
        "development_editable": development_editable_offline(),
        "published_resolution": published_resolution_offline(),
        "uv_workspace_sync": uv_workspace_sync_offline(),
    }
