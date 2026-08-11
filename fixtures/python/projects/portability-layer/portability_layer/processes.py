"""Subprocesses and quoting (PY-CAN-PLAT-007)."""

from __future__ import annotations

import os
import shlex
import subprocess
import sys
import tempfile
from dataclasses import dataclass


@dataclass(frozen=True)
class ProcessResult:
    argv: list[str]
    returncode: int
    stdout: str | bytes
    stderr: str | bytes
    text_mode: bool


def run_with_argv(argv: list[str], env: dict[str, str] | None = None) -> ProcessResult:
    """Spawn current interpreter with an explicit argument vector."""
    code = "import sys, json; json.dump(sys.argv, sys.stdout)"
    proc = subprocess.run(
        [sys.executable, "-c", code, *argv],
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )
    return ProcessResult(argv=argv, returncode=proc.returncode, stdout=proc.stdout, stderr=proc.stderr, text_mode=True)


def run_text_mode(argv: list[str]) -> ProcessResult:
    """Spawn with text I/O, capturing stdout as str, testing communicate semantics."""
    code = "import sys; print(' '.join(sys.argv[1:])); print('stderr line', file=sys.stderr)"
    proc = subprocess.run(
        [sys.executable, "-c", code, *argv],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="strict",
        check=False,
    )
    # Also demonstrate Popen + communicate to avoid deadlock pattern
    with subprocess.Popen(
        [sys.executable, "-c", "import sys; data=sys.stdin.read(); sys.stdout.write(data.upper())"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
    ) as popen:
        out, err = popen.communicate(input="hello via stdin")
        _ = (out, err)
    return ProcessResult(argv=argv, returncode=proc.returncode, stdout=proc.stdout, stderr=proc.stderr, text_mode=True)


def run_bytes_mode(argv: list[str]) -> ProcessResult:
    """Spawn with bytes I/O, capturing stdout as bytes."""
    code = "import sys; sys.stdout.buffer.write(b'bytes:' + b' '.join(a.encode() for a in sys.argv[1:]))"
    proc = subprocess.run(
        [sys.executable, "-c", code, *argv],
        capture_output=True,
        text=False,
        check=False,
    )
    return ProcessResult(argv=argv, returncode=proc.returncode, stdout=proc.stdout, stderr=proc.stderr, text_mode=False)


def run_with_environment(extra: dict[str, str]) -> ProcessResult:
    """Spawn with custom environment and demonstrate inheritance."""
    env = os.environ.copy()
    env.update(extra)
    code = "import os; import json; json.dump(dict(os.environ), sys.stdout)"  # type: ignore[name-defined]
    # Need sys import in code
    code2 = "import os, sys, json; json.dump({k: os.environ[k] for k in sorted(os.environ) if k.startswith('PORTABILITY_')}, sys.stdout)"
    proc = subprocess.run(
        [sys.executable, "-c", code2],
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )
    return ProcessResult(argv=[], returncode=proc.returncode, stdout=proc.stdout, stderr=proc.stderr, text_mode=True)


def run_exit_code(code_value: int) -> ProcessResult:
    """Spawn a child that exits with a specific code and report returncode."""
    proc = subprocess.run(
        [sys.executable, "-c", f"import sys; sys.exit({code_value})"],
        capture_output=True,
        text=True,
        check=False,
    )
    return ProcessResult(argv=[], returncode=proc.returncode, stdout=proc.stdout, stderr=proc.stderr, text_mode=True)


def run_shell_guarded(command: str) -> ProcessResult | None:
    """Guarded shell command case (POSIX shell via shell=True).

    Returns None when not on POSIX to keep coverage guarded.
    """
    if os.name != "posix":
        return None
    # Use shell quoting to avoid injection; this is the safe pattern.
    quoted = shlex.quote(command)
    # Actually run via shell with a safe echo through shell expansion
    proc = subprocess.run(
        f"echo {quoted}",
        shell=True,
        capture_output=True,
        text=True,
        check=False,
    )
    # Also demonstrate shlex.split for argument-vector safety
    _argv = shlex.split(f"echo {quoted}")
    return ProcessResult(argv=_argv, returncode=proc.returncode, stdout=proc.stdout, stderr=proc.stderr, text_mode=True)


def demonstrate_quoting_and_shell() -> dict[str, object]:
    with tempfile.TemporaryDirectory() as td:
        tmp_env = {"PORTABILITY_TMP": td, "PORTABILITY_FLAG": "1"}
        return {
            "argv_echo": run_with_argv(["hello", "world with spaces", "arg\twith\ttabs"]),
            "text_mode": run_text_mode(["text-case"]),
            "bytes_mode": run_bytes_mode(["bytes-case"]),
            "env": run_with_environment(tmp_env),
            "exit_0": run_exit_code(0),
            "exit_2": run_exit_code(2),
            "shell_guarded": run_shell_guarded("hello; echo injected"),
            "executable_lookup": subprocess.run(
                [sys.executable, "-c", "import sys; print(sys.executable)"],
                capture_output=True,
                text=True,
                check=False,
            ).stdout.strip(),
        }
