"""Pure-Python app module inside zip."""

from __future__ import annotations

from importlib import resources

PACKAGE = "native_app"


def greet() -> str:
    return "native-app: hello from zip"


def get_data() -> str:
    # importlib.resources works from zipimport
    return resources.files(PACKAGE).joinpath("data.txt").read_text(encoding="utf-8").strip()


def main() -> None:
    print(greet())
    print(get_data())


if __name__ == "__main__":
    main()
