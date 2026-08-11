"""Generate version artifact for PY-CAN-INT-005 and PY-CAN-PKG-003."""

from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
INPUT = ROOT / "generator" / "version_input.json"
OUTPUTS = [
    ROOT / "distributions" / "suite_core" / "suite_core" / "_generated_version.py",
    ROOT / "distributions" / "suite_src" / "src" / "suite_src" / "_generated_version.py",
]

TEMPLATE = '''"""Generated version — do not edit. Source: generator/version_input.json."""

__version__ = "{version}"
__release_date__ = "{release_date}"
__commit__ = "{commit}"
__generated__ = True
'''


def main() -> None:
    data = json.loads(INPUT.read_text(encoding="utf-8"))
    content = TEMPLATE.format(**data)
    for out in OUTPUTS:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(content, encoding="utf-8")
        print(f"generated {out.relative_to(ROOT)} -> {data['version']}")


if __name__ == "__main__":
    main()
