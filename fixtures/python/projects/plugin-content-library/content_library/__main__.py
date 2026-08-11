"""Package ``__main__`` entry point (PY-CAN-MOD-001).

Executed via ``python -m content_library``.  Reuses the declaration-bearing
``entry_declarations`` module so the same declarations are reachable through
both the submodule and the package entry point.
"""

from __future__ import annotations

from content_library.entry_declarations import ContentItem, create_item, module_identity


def main() -> None:
    ident = module_identity()
    item = create_item("main-entry", kind="package-main")
    print(f"package __main__ identity: {ident}")
    print(f"created {item!r} via {ContentItem.__module__}")
    if __name__ == "__main__":
        # Demonstrates the package main guard inside ``__main__.py``.
        print("executed via python -m content_library")


if __name__ == "__main__":
    main()
