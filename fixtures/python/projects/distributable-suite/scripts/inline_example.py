# /// script
# requires-python = ">=3.10"
# dependencies = ["requests>=2.28.1"]
# ///

"""PEP 723 inline-script metadata block run offline through the installed runner (uv).

Run offline:

    uv run --offline --with requests scripts/inline_example.py

The block above declares Python version and dependencies; runner creates ephemeral
environment and executes script. `import requests` succeeds only when metadata
declares it; undeclared dependency would fail.

Import versus direct execution: `python scripts/inline_example.py` runs as
`__main__` with __package__ is None; `python -m scripts.inline_example` would
differ, but PEP 723 runner uses direct execution identity.

Ephemeral environment is discarded after run.
"""

import sys

def main() -> int:
    print(f"inline script run on {sys.version.split()[0]}")
    try:
        import requests

        print(f"requests {requests.__version__} available via PEP 723")
    except ImportError as e:
        print(f"requests missing: {e}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
