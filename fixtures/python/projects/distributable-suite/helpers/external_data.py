"""PKG-012 external data scheme (data_files outside site-packages)."""

from __future__ import annotations
import pathlib
import sysconfig
import sys

# Declared via [tool.setuptools.data-files] "share/suite_core" = ["suite_core/resources/data.txt"]
# After install, file lands at sysconfig.get_path("data") + "/share/suite_core/data.txt"
# Not part of package's __file__ tree, but accessible via data scheme.


def data_file_installed_path() -> pathlib.Path:
    data_root = pathlib.Path(sysconfig.get_path("data"))
    return data_root / "share" / "suite_core" / "data.txt"


def verify_external_scheme(venv: pathlib.Path | None = None) -> bool:
    import subprocess, pathlib, sys
    if venv is None:
        # Check in current env after pip install offline
        return data_file_installed_path().exists()
    bin_dir = "Scripts" if sys.platform == "win32" else "bin"
    py = venv / bin_dir / "python"
    code = "import sysconfig, pathlib; print(pathlib.Path(sysconfig.get_path('data'))/'share'/'suite_core'/'data.txt')"
    result = subprocess.run([str(py), "-c", code], capture_output=True, text=True)
    path = pathlib.Path(result.stdout.strip())
    return path.exists()
