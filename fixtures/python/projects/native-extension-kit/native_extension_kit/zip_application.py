"""PY-CAN-NATIVE-010: executable zip application variants."""

from __future__ import annotations

import pathlib
import subprocess
import sys
import sysconfig
import tempfile
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
        "timestamp_reproducibility": "zip entries use fixed timestamp 1980-01-01 for reproducibility; see Taskfile zip creation",
    }


def native_in_zip_failure_demo() -> dict[str, object]:
    suffix = sysconfig.get_config_var("EXT_SUFFIX") or ".so"
    so_path = pathlib.Path(__file__).with_name(f"_native_single{suffix}")
    if not so_path.exists():
        return {"available": False, "reason": f"native artifact not built: {so_path.name}"}
    with tempfile.TemporaryDirectory() as tmp:
        zip_path = pathlib.Path(tmp) / "native_test.zip"
        with zipfile.ZipFile(str(zip_path), "w") as zf:
            zf.write(str(so_path), f"native_pkg/_native_single{suffix}")
            # also add minimal __init__ to make package
            zf.writestr("native_pkg/__init__.py", "")
        # Attempt import from zip in subprocess to avoid polluting sys.path
        code = f"""
import sys, pathlib, importlib.util
zip_path = pathlib.Path({str(zip_path)!r})
sys.path.insert(0, str(zip_path))
try:
    import native_pkg._native_single
    print("unexpected: imported")
except ImportError as e:
    print(f"ImportError:{{e}}")
except Exception as e:
    print(f"{{type(e).__name__}}:{{e}}")
finally:
    sys.path.remove(str(zip_path))
"""
        proc = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, timeout=5)
        return {
            "available": True,
            "zip": str(zip_path),
            "stdout": proc.stdout.strip(),
            "stderr": proc.stderr.strip(),
            "returncode": proc.returncode,
            "note": "native extension in zip fails: zipimport cannot load extension module",
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


__all__ = ["build_info", "native_in_zip_failure_demo", "run_zipapp_demo", "zip_contents_demo", "DIST_ZIP"]
