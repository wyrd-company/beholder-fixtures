"""Module and console entry modes (PY-CAN-INT-007).

- Module mode: `python -m feature_integration_suite.mp_entry`
- Console mode: `feature-suite-worker` via [project.scripts] or `python feature_integration_suite/mp_entry.py`
"""

from __future__ import annotations

import multiprocessing
import sys

from feature_integration_suite.mp_workers import spawn_spawn_demo, worker


def main() -> None:
    multiprocessing.freeze_support()
    # Demonstrate console entry can spawn without recursion because worker is top-level importable
    result = spawn_spawn_demo()
    print(f"console-entry:{result} module:{worker.__module__}")


if __name__ == "__main__":
    # This guard prevents recursive spawn when child imports __main__ under spawn
    main()
