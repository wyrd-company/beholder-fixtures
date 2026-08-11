"""PY-CAN-DYN-006 generated console launcher."""

from __future__ import annotations

import pathlib
import sys
import sysconfig

# Declared script target: suite_core.cli:main via [project.scripts] suite-tool
# After install, pip generates wrapper:
# - POSIX: <venv>/bin/suite-tool (shebang + import)
# - Windows: <venv>/Scripts/suite-tool.exe (stub)
# Invocation: suite-tool arg1 arg2  -> main(argv) with argv[0] as script name

WRAPPER_POSIX = pathlib.Path(sysconfig.get_path("scripts")) / "suite-tool"


def invoke_wrapper(args: list[str]) -> int:
    from suite_core.cli import main

    return main(args)


def argv0_note() -> str:
    return "argv[0] is wrapper path, not module path; module execution `python -m suite_core.cli` differs"


def malformed_reference_note() -> str:
    return "malformed entry point suite_core.cli:missing would fail at install metadata validation"
