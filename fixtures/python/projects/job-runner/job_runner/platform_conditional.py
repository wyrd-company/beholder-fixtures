"""Additional file to show source parser accepts all live files (PY-CAN-FLOW-013)."""

from __future__ import annotations

import sys

# This file exists to demonstrate that conditional definition branches across
# multiple files all parse under the selected interpreter, even when
# platform-specific branches are not taken.

if sys.platform == "win32":
    def platform_job_runner() -> str:
        return "windows-runner"
else:
    def platform_job_runner() -> str:
        return "posix-runner"


# Availability-gated import with fallback — both branches parse.
try:
    import asyncio as _asyncio  # noqa: F401

    async_available = True
except ImportError:
    async_available = False
