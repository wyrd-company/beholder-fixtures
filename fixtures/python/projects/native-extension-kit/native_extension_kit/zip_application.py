"""PY-CAN-NATIVE-010: executable zip application variants."""

from __future__ import annotations

import pathlib
import subprocess
import sys
import zipfile

DIST_ZIP = pathlib.Path(__file__).parent.parent / "dist" / "native_app.pyz"
SRC_ROOT = pathlib.Path(__file__).parent.parent / "zip_src" / "native_app"


def build_info() -> dict[str, object]:
    return {
        "archive_root_main": "__main__.py",
        "pure_python_imports": "native_app.app imports importlib.resources",
        "resources": "native_app/data.txt via importlib.resources",
        "shebang": "#!/usr/bin/env python3 (zipapp shebang variant)",
        "bundled_dependency": "native_app package bundled inside zip",
        "external_dependency": "stdlib only; external stdlib import remains outside zip",
        "native_failure": "extension modules (_native_single) cannot be imported from zip (ImportError)",
        "timestamp_reproducibility": "zip entries use fixed timestamp 1980-01-01 for reproducibility; see Taskfile zip creation",
    }


def run_zipapp_demo() -> dict[str, object]:
    if not DIST_ZIP.exists():
        return {"available": False, "reason": f"zip not built: {DIST_ZIP}"}
    proc = subprocess.run([sys.executable, str(DIST_ZIP)], capture_output=True, text=True, timeout=5)
    return {
        "available": True,
        "returncode": proc.returncode,
        "stdout": proc.stdout.strip(),
        "stderr": proc.stderr.strip(),
    }


def zip_contents_demo() -> dict[str, object]:
    if not DIST_ZIP.exists():
        return {"available": False}
    with zipfile.ZipFile(str(DIST_ZIP)) as zf:
        names = zf.namelist()
    return {"names": sorted(names), "has_main": "__main__.py" in names, "has_app": "native_app/app.py" in names}


__all__ = ["build_info", "run_zipapp_demo", "zip_contents_demo", "DIST_ZIP"]
