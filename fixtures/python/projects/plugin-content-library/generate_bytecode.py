"""Generate the committed byte-compiled, source-less module (PY-CAN-MOD-017).

Reads ``bytecode_src/source_for_bytecode.py`` and writes a ``.pyc``
loadable via :class:`importlib.machinery.SourcelessFileLoader` so the
module can be imported without its source.

The output is ``content_library/generated_bytecode/bytecode_only.pyc``,
committed to the repository. ``task build`` and validation do not invoke
this script.
"""

from __future__ import annotations

import pathlib
import py_compile
import importlib.util

SRC = pathlib.Path(__file__).parent / "bytecode_src" / "source_for_bytecode.py"
OUT_DIR = pathlib.Path(__file__).parent / "content_library" / "generated_bytecode"
OUT = OUT_DIR / "bytecode_only.pyc"


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    # Compile to a sourceless loader-friendly .pyc (not __pycache__).
    # Use dfile to embed the original filename for traceback, but no source copy.
    py_compile.compile(str(SRC), cfile=str(OUT), dfile=str(SRC), doraise=True)
    # Verify the output can be loaded.
    magic = importlib.util.MAGIC_NUMBER  # keep reference to show bytecode nature
    print(f"generated {OUT} (magic={magic.hex()})")
    # Also ensure the compiled file is importable.
    import importlib.machinery as machinery

    machinery_loader = machinery.SourcelessFileLoader("content_library.generated_bytecode.bytecode_only", str(OUT))
    spec = machinery.ModuleSpec("content_library.generated_bytecode.bytecode_only", machinery_loader, origin=str(OUT))
    mod = importlib.util.module_from_spec(spec)
    machinery_loader.exec_module(mod)
    assert getattr(mod, "VALUE", None) == "bytecode-only-value", "generated module VALUE mismatch"
    print(f"verified VALUE={mod.VALUE}")


if __name__ == "__main__":
    main()
