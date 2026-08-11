"""Dynamic import APIs (PY-CAN-MOD-013).

- constant, composed, and configuration-derived module names via ``importlib``
- one ``__import__`` variant
- relative dynamic import
- ``spec_from_file_location``
- missing/invalid name handling
- ``sys.modules`` substitution
- unresolved computed target
"""

from __future__ import annotations

import importlib
import importlib.util
import pathlib
import sys
import types

# Constant dynamic import.
constant_import = importlib.import_module("content_library.registry")

# Composed name via string formatting.
_prefix = "content_library"
_name = "entry_declarations"
composed_import = importlib.import_module(f"{_prefix}.{_name}")

# Configuration-derived module name.
CONFIG = {"plugin": "content_library.conditional_imports"}
config_import = importlib.import_module(CONFIG["plugin"])

# ``__import__`` variant.
builtin_import = __import__("content_library.registry", fromlist=["CONTENT_REGISTRY"])

# Relative dynamic import via ``package`` argument.
relative_dynamic = importlib.import_module(".entry_declarations", package="content_library")

# ``spec_from_file_location`` for an ad-hoc module not on sys.path.
def spec_from_file_demo() -> types.ModuleType:
    path = pathlib.Path(__file__).with_name("entry_declarations.py")
    spec = importlib.util.spec_from_file_location("ad_hoc_entry", str(path))
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore
    return mod


def missing_name_demo() -> str:
    try:
        importlib.import_module("content_library.nonexistent_dynamic")
        return "unexpected-success"
    except ModuleNotFoundError as exc:
        return f"missing:{exc.name}"


def invalid_name_demo() -> str:
    try:
        importlib.import_module("content library.bad-name")
        return "unexpected-success"
    except (ModuleNotFoundError, ImportError, ValueError) as exc:
        return f"invalid:{exc.__class__.__name__}"


def sys_modules_substitution_demo() -> str:
    fake_name = "content_library.synthetic_injected"
    fake_module = types.ModuleType(fake_name)
    fake_module.INJECTED = "synthetic-value"  # type: ignore
    sys.modules[fake_name] = fake_module
    try:
        imported = importlib.import_module(fake_name)
        return imported.INJECTED  # type: ignore
    finally:
        del sys.modules[fake_name]


# Unresolved computed target — graph cannot statically resolve ``target`` derived from variable.
def unresolved_dynamic(target: str) -> str:
    module = importlib.import_module(target)
    return module.__name__
