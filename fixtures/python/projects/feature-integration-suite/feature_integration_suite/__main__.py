"""Package entry mode (PY-CAN-INT-007): `python -m feature_integration_suite`."""

from __future__ import annotations

import multiprocessing

from feature_integration_suite.mp_workers import spawn_spawn_demo

if __name__ == "__main__":
    multiprocessing.freeze_support()
    result = spawn_spawn_demo()
    print(f"package-main:{result}")
