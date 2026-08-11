"""Audit hooks (PY-CAN-DIAG-018).

Registers a narrow audit hook in an isolated child and causes
import, file, and compile events.
"""

from __future__ import annotations

import subprocess
import sys
import textwrap


def _child_audit_script() -> str:
    return textwrap.dedent(
        """
        import sys
        import tempfile
        import pathlib

        events = []

        def hook(event, args):
            # Narrow filter: only import, open, and compile (or exec/compile variants)
            if event in {"import", "open", "compile"} or event.startswith("import") or event.startswith("open") or event.startswith("compile"):
                events.append(event)
            # Also capture exact names for file-related events
            if event == "open":
                events.append(f"open:{args[0][:50] if args and args else ''}")

        sys.addaudithook(hook)

        # Cause import event
        import importlib
        import json  # triggers import audit

        # Cause file event (open)
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as tf:
            tf.write("audit demo")
            tmpname = tf.name
        with open(tmpname, "r") as f:
            _ = f.read()
        pathlib.Path(tmpname).unlink(missing_ok=True)

        # Cause compile event
        compile("x = 1 + 2", "<audit>", "exec")
        exec("y = 2 + 3")

        # Report
        # Deduplicate but keep order
        seen = []
        for e in events:
            if e not in seen:
                seen.append(e)
        for e in seen:
            print(e)
        print(f"import_seen:{any(e.startswith('import') for e in seen)}")
        print(f"open_seen:{any(e.startswith('open') for e in seen)}")
        print(f"compile_seen:{any(e.startswith('compile') for e in seen)}")
        """
    )


def run_isolated_audit_demo() -> dict[str, object]:
    """Run narrow audit hook in an isolated child process."""

    result = subprocess.run(
        [sys.executable, "-c", _child_audit_script()],
        capture_output=True,
        text=True,
        check=False,
    )
    stdout_lines = result.stdout.strip().splitlines() if result.stdout else []
    return {
        "returncode": result.returncode,
        "stdout": stdout_lines,
        "stderr": result.stderr.strip(),
        "import_seen": any("import_seen:True" in l for l in stdout_lines),
        "open_seen": any("open_seen:True" in l for l in stdout_lines),
        "compile_seen": any("compile_seen:True" in l for l in stdout_lines),
    }


def demo_narrow_hook_filters() -> dict[str, object]:
    """Show narrow hook does not capture unrelated events."""

    code = textwrap.dedent(
        """
        import sys
        events=[]
        def hook(event, args):
            if event in {"import", "open", "compile"}:
                events.append(event)
        sys.addaudithook(hook)
        # These should not be captured if hook is narrow (they are captured only if in set)
        # But we test that hook is installed and import triggers.
        import json
        print("import" in events)
        print("unrelated_not_captured", "socket" not in events)
        """
    )
    result = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, check=False)
    return {"stdout": result.stdout.strip().splitlines(), "stderr": result.stderr.strip()}


def all_audit_demos() -> dict[str, object]:
    """Collect audit hook demos."""

    return {
        "isolated": run_isolated_audit_demo(),
        "narrow": demo_narrow_hook_filters(),
    }
