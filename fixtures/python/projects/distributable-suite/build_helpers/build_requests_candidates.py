"""Rebuild the offline requests candidate placeholders for PKG-019 and PKG-021.

These are local, download-free placeholders for the ``requests`` name used by the
offline candidate set. The module exposes ``__version__`` so the PKG-021 inline
script (which prints ``requests.__version__``) runs to completion offline. Run
manually to regenerate the committed wheels; this is not part of required
validation.
"""

from __future__ import annotations

import base64
import hashlib
import pathlib
import zipfile

ROOT = pathlib.Path(__file__).parents[1]
CANDIDATES = ROOT / "candidate_set"

WHEEL = "Wheel-Version: 1.0\nGenerator: fixture\nRoot-Is-Purelib: true\nTag: py3-none-any\n"


def _record_line(name: str, data: bytes) -> str:
    digest = base64.urlsafe_b64encode(hashlib.sha256(data).digest()).rstrip(b"=").decode()
    return f"{name},sha256={digest},{len(data)}"


def build(version: str, out_dir: pathlib.Path) -> pathlib.Path:
    dist_info = f"requests-{version}.dist-info"
    init = f'"""Offline placeholder for the requests name."""\n\n__version__ = "{version}"\n'.encode()
    metadata = (
        f"Metadata-Version: 2.1\nName: requests\nVersion: {version}\n"
        "Summary: offline placeholder for candidate set\n"
    ).encode()
    wheel_meta = WHEEL.encode()

    files = {
        "requests/__init__.py": init,
        f"{dist_info}/METADATA": metadata,
        f"{dist_info}/WHEEL": wheel_meta,
    }
    record_name = f"{dist_info}/RECORD"
    record_body = "\n".join(_record_line(n, d) for n, d in files.items())
    record_body += f"\n{record_name},,\n"
    files[record_name] = record_body.encode()

    out_dir.mkdir(parents=True, exist_ok=True)
    wheel_path = out_dir / f"requests-{version}-py3-none-any.whl"
    with zipfile.ZipFile(wheel_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for name, data in files.items():
            zf.writestr(name, data)
    return wheel_path


def main() -> None:
    print(build("2.31.0", CANDIDATES / "satisfiable"))
    print(build("2.25.0", CANDIDATES / "conflict"))


if __name__ == "__main__":
    main()
