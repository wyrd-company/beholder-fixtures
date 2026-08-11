"""Pure-Python app module inside zip."""

from __future__ import annotations

from importlib import resources

PACKAGE = "native_app"


def greet() -> str:
    return "native-app: hello from zip"


def get_data() -> str:
    # importlib.resources works from zipimport
    return resources.files(PACKAGE).joinpath("data.txt").read_text(encoding="utf-8").strip()


def try_native_import() -> str:
    try:
        import importlib.util
        # Attempt to import extension from zip: zipimport cannot load .so from archive
        # Simulate bundled native by searching for _native_single inside zip
        spec = importlib.util.find_spec("native_app._native_single")
        if spec is None:
            return "ImportError: native extension not loadable from zip (find_spec returned None)"
        return f"unexpected: found {spec.origin}"
    except ImportError as exc:
        return f"ImportError: {exc}"
    except Exception as exc:
        return f"{type(exc).__name__}: {exc}"


def main() -> None:
    print(greet())
    print(get_data())
    print(try_native_import())


if __name__ == "__main__":
    main()
