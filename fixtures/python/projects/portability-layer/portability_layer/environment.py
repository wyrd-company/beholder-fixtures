"""Environment and startup configuration (PY-CAN-PLAT-005)."""

from __future__ import annotations

import os
import pathlib
import subprocess
import sys
import tempfile
from dataclasses import dataclass


@dataclass(frozen=True)
class StartupProbe:
    argv: list[str]
    env: dict[str, str]
    hash_seed: str | None
    utf8_mode: int | None
    warning_filter: str | None


def _run_child(extra_args: list[str], extra_env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env.update(extra_env)
    code = (
        "import os, sys, warnings; "
        "print('executable=' + sys.executable); "
        "print('hash_seed=' + str(os.environ.get('PYTHONHASHSEED'))); "
        "print('utf8=' + str(sys.flags.utf8_mode)); "
        "print('warnopts=' + str(sys.warnoptions)); "
        "print('path_has_extra=' + str(any('portability-probe' in p for p in sys.path))); "
        "print('isolated=' + str(sys.flags.isolated)); "
    )
    return subprocess.run(
        [sys.executable, *extra_args, "-c", code],
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )


def spawn_with_hash_seed(seed: str) -> subprocess.CompletedProcess[str]:
    """Child with controlled PYTHONHASHSEED (random, fixed, disabled)."""
    return _run_child([], {"PYTHONHASHSEED": seed})


def spawn_with_utf8_setting(mode: str) -> subprocess.CompletedProcess[str]:
    """Child varying PYTHONUTF8 (0/1)."""
    return _run_child([], {"PYTHONUTF8": mode})


def spawn_with_warning_flag(filter_expr: str) -> subprocess.CompletedProcess[str]:
    """Child varying warning configuration via -W."""
    return _run_child(["-W", filter_expr], {})


def spawn_with_pythonpath(tmpdir: pathlib.Path) -> subprocess.CompletedProcess[str]:
    """Child varying PYTHONPATH."""
    probe_dir = tmpdir / "portability-probe"
    probe_dir.mkdir(parents=True, exist_ok=True)
    (probe_dir / "probe_marker.py").write_text("MARKER=1\n", encoding="utf-8")
    env = {"PYTHONPATH": str(probe_dir) + os.pathsep + os.environ.get("PYTHONPATH", "")}
    return _run_child([], env)


def spawn_isolated() -> subprocess.CompletedProcess[str]:
    """Child in isolated mode (-I) where PYTHONPATH and user site are ignored."""
    with tempfile.TemporaryDirectory() as td:
        probe = pathlib.Path(td) / "portability-probe"
        probe.mkdir()
        env = {"PYTHONPATH": str(probe)}
        result = _run_child(["-I"], env)
        return result


def spawn_no_user_site() -> subprocess.CompletedProcess[str]:
    """Child with -s (no user site)."""
    return _run_child(["-s"], {})


def spawn_no_site() -> subprocess.CompletedProcess[str]:
    """Child with -S (no site)."""
    return _run_child(["-S"], {})


def spawn_with_application_setting() -> subprocess.CompletedProcess[str]:
    """Child varying an application-level setting via env (APP_MODE)."""
    env = {"APP_MODE": "portability-layer-test", "APP_FEATURE": "enabled"}
    code = "import os; print(os.environ.get('APP_MODE')); print(os.environ.get('APP_FEATURE'))"
    full_env = os.environ.copy()
    full_env.update(env)
    return subprocess.run(
        [sys.executable, "-c", code],
        capture_output=True,
        text=True,
        env=full_env,
        check=False,
    )


def spawn_with_env(extra_env: dict[str, str], code: str = "import os; print(sorted(os.environ.keys())[:3])") -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env.update(extra_env)
    return subprocess.run(
        [sys.executable, "-c", code],
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )


def demonstrate_startup_variants() -> dict[str, object]:
    """Collect controlled child interpreter variants for coverage."""
    with tempfile.TemporaryDirectory() as td:
        tmp = pathlib.Path(td)
        return {
            "hash_random": spawn_with_hash_seed("random").stdout.strip().splitlines()[:2],
            "hash_fixed": spawn_with_hash_seed("42").stdout.strip().splitlines()[:2],
            "hash_disabled": spawn_with_hash_seed("0").stdout.strip().splitlines()[:2],
            "utf8_0": spawn_with_utf8_setting("0").stdout.strip().splitlines()[:3],
            "utf8_1": spawn_with_utf8_setting("1").stdout.strip().splitlines()[:3],
            "warn_error": spawn_with_warning_flag("error::DeprecationWarning").stdout.strip(),
            "pythonpath": spawn_with_pythonpath(tmp).stdout.strip().splitlines()[:4],
            "isolated": spawn_isolated().stdout.strip().splitlines()[:4],
            "no_user_site": spawn_no_user_site().stdout.strip().splitlines()[:2],
            "no_site": spawn_no_site().stdout.strip().splitlines()[:2],
            "app_settings": spawn_with_application_setting().stdout.strip(),
        }
