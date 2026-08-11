"""Security-sensitive dynamic APIs (PY-CAN-DIAG-017).

Benign guard and counterexample cases for eval/exec, pickle, shell,
dynamic import, archive extraction, and deserialization without
exploit payloads.
"""

from __future__ import annotations

import ast
import importlib
import io
import json
import pickle
import shlex
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# eval / exec guards
# ---------------------------------------------------------------------------


def guarded_eval(expression: str, allowed_names: set[str] | None = None) -> Any:
    """Guarded eval that allows only arithmetic and whitelisted names."""

    allowed_names = allowed_names or set()
    tree = ast.parse(expression, mode="eval")
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and node.id not in allowed_names:
            raise ValueError(f"name not allowed: {node.id}")
        if isinstance(node, (ast.Import, ast.ImportFrom, ast.Call)):
            # Only allow calls to whitelisted names; for demo, disallow all calls unless name in allowlist
            if isinstance(node, ast.Call) and not (
                isinstance(node.func, ast.Name) and node.func.id in allowed_names
            ):
                raise ValueError("call not allowed")
    # Use empty builtins for safety; no exploit payload.
    return eval(compile(tree, "<guarded>", "eval"), {"__builtins__": {}}, {n: 0 for n in allowed_names})


def counterexample_raw_eval(expression: str) -> Any:
    """Counterexample: raw eval without guard (used only on benign input)."""

    return eval(expression, {"__builtins__": {}}, {})


def guarded_exec(code: str, allowed_names: set[str] | None = None) -> dict[str, Any]:
    """Guarded exec allowing only assignments and arithmetic."""

    allowed_names = allowed_names or set()
    tree = ast.parse(code, mode="exec")
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            raise ValueError("import not allowed")
        if isinstance(node, ast.Name) and node.id not in allowed_names and node.id not in {"result"}:
            # Allow only whitelisted or result
            if isinstance(node.ctx, ast.Store):
                continue
            raise ValueError(f"name not allowed: {node.id}")
    namespace: dict[str, Any] = {}
    exec(compile(tree, "<guarded>", "exec"), {"__builtins__": {}}, namespace)  # noqa: S102
    return namespace


def counterexample_raw_exec(code: str) -> dict[str, Any]:
    """Counterexample: raw exec without guard (benign code only)."""

    ns: dict[str, Any] = {}
    exec(code, {"__builtins__": {}}, ns)  # noqa: S102
    return ns


# ---------------------------------------------------------------------------
# pickle guards
# ---------------------------------------------------------------------------


class GuardedUnpickler(pickle.Unpickler):
    """Unpickler that only allows safe built-in types."""

    allowed = {"builtins": {"list", "dict", "set", "str", "int", "float", "tuple"}}

    def find_class(self, module: str, name: str) -> Any:  # type: ignore[override]
        if module in self.allowed and name in self.allowed[module]:
            return super().find_class(module, name)
        raise pickle.UnpicklingError(f"forbidden: {module}.{name}")


def guarded_pickle_roundtrip(obj: Any) -> Any:
    """Pickle with guarded unpickling."""

    data = pickle.dumps(obj)
    return GuardedUnpickler(io.BytesIO(data)).load()


def counterexample_raw_pickle(obj: Any) -> Any:
    """Counterexample: raw pickle load (benign data only)."""

    data = pickle.dumps(obj)
    return pickle.loads(data)  # noqa: S301


# ---------------------------------------------------------------------------
# shell guard
# ---------------------------------------------------------------------------


def guarded_shell_command(filename: str) -> subprocess.CompletedProcess[str]:
    """Run a shell command with guarded argument quoting (no shell=True)."""

    # Benign guard: treat filename as data, not code, via list form and shlex.
    safe = shlex.quote(filename)
    # Use shell=False with explicit argv; no injection.
    return subprocess.run(
        [sys.executable, "-c", "import sys; print(sys.argv[1])", safe],
        capture_output=True,
        text=True,
        check=False,
    )


def counterexample_shell_true(filename: str) -> subprocess.CompletedProcess[str]:
    """Counterexample: shell=True with string interpolation (benign filename only).

    This demonstrates the unsafe pattern without an exploit payload; the
    filename is still benign, but the construction is shell-sensitive.
    """

    # Intentionally shell=True for contrast; we pass a constant benign filename.
    return subprocess.run(
        f"{shlex.quote(sys.executable)} -c 'import sys; print(1)'",
        shell=True,  # noqa: S602
        capture_output=True,
        text=True,
        check=False,
    )


# ---------------------------------------------------------------------------
# dynamic import guard
# ---------------------------------------------------------------------------


def guarded_dynamic_import(name: str, allowlist: set[str] | None = None) -> Any:
    """Import only if name is in explicit allowlist."""

    allowlist = allowlist or {"diagnostics_toolkit.warnings_toolkit", "json", "pathlib"}
    if name not in allowlist:
        raise ValueError(f"import not allowed: {name}")
    return importlib.import_module(name)


def counterexample_raw_dynamic_import(name: str) -> Any:
    """Counterexample: dynamic import without guard (benign name only)."""

    return importlib.import_module(name)


# ---------------------------------------------------------------------------
# archive extraction guard
# ---------------------------------------------------------------------------


def guarded_archive_extract(archive_path: Path, dest: Path) -> list[str]:
    """Extract tar safely, rejecting path-traversal entries."""

    extracted: list[str] = []
    with tarfile.open(archive_path, "r") as tf:
        for member in tf.getmembers():
            member_path = (dest / member.name).resolve()
            if not str(member_path).startswith(str(dest.resolve())):
                raise ValueError(f"path traversal: {member.name}")
            tf.extract(member, dest, filter="data")  # type: ignore[arg-type]
            extracted.append(member.name)
    return extracted


def counterexample_raw_extract(archive_path: Path, dest: Path) -> list[str]:
    """Counterexample: raw extraction without traversal check (benign archive only)."""

    with tarfile.open(archive_path, "r") as tf:
        tf.extractall(dest, filter="data")  # type: ignore[arg-type]
        return tf.getnames()


def _build_benign_tar(path: Path) -> None:
    with tarfile.open(path, "w") as tf:
        info = tarfile.TarInfo(name="benign.txt")
        data = b"benign content"
        info.size = len(data)
        tf.addfile(info, io.BytesIO(data))


# ---------------------------------------------------------------------------
# deserialization guard (json vs pickle)
# ---------------------------------------------------------------------------


def guarded_json_deserialize(payload: str) -> Any:
    """Guarded deserialization via json with strict parsing."""

    return json.loads(payload)


def counterexample_pickle_deserialize(payload: bytes) -> Any:
    """Counterexample: pickle deserialization (benign payload only)."""

    return pickle.loads(payload)  # noqa: S301


def all_security_demos() -> dict[str, object]:
    """Run benign guard/counterexample demos."""

    # eval
    guarded_eval_result = guarded_eval("1 + 2", allowed_names=set())
    try:
        guarded_eval("__import__('os')", allowed_names=set())
        eval_guard_blocked = False
    except (ValueError, SyntaxError):
        eval_guard_blocked = True

    # exec
    guarded_exec_result = guarded_exec("result = 1 + 2")
    try:
        guarded_exec("import os")
        exec_guard_blocked = False
    except ValueError:
        exec_guard_blocked = True

    # pickle
    pickle_guarded = guarded_pickle_roundtrip({"a": [1, 2]})

    # shell
    shell_guarded = guarded_shell_command("benign.txt")
    shell_counter = counterexample_shell_true("benign.txt")

    # dynamic import
    dynamic_guarded = guarded_dynamic_import("json")
    try:
        guarded_dynamic_import("os")
        dynamic_blocked = False
    except ValueError:
        dynamic_blocked = True

    # archive
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        archive = tmp_path / "benign.tar"
        _build_benign_tar(archive)
        dest = tmp_path / "dest"
        dest.mkdir()
        guarded_names = guarded_archive_extract(archive, dest)
        # Rebuild for raw
        archive2 = tmp_path / "benign2.tar"
        _build_benign_tar(archive2)
        dest2 = tmp_path / "dest2"
        dest2.mkdir()
        raw_names = counterexample_raw_extract(archive2, dest2)

    # json
    json_guarded = guarded_json_deserialize('{"key": "value"}')

    return {
        "eval_guarded": guarded_eval_result,
        "eval_blocked": eval_guard_blocked,
        "exec_guarded": guarded_exec_result.get("result"),
        "exec_blocked": exec_guard_blocked,
        "pickle_guarded": pickle_guarded,
        "shell_guarded_rc": shell_guarded.returncode,
        "shell_counter_rc": shell_counter.returncode,
        "dynamic_guarded": dynamic_guarded.__name__ if hasattr(dynamic_guarded, "__name__") else str(dynamic_guarded),
        "dynamic_blocked": dynamic_blocked,
        "archive_guarded": guarded_names,
        "archive_raw": raw_names,
        "json_guarded": json_guarded,
    }
