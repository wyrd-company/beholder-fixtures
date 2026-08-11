"""Console script target for PY-CAN-DYN-006."""

from __future__ import annotations

import sys


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    print(f"suite-tool invoked with {args!r}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
