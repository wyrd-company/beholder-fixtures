"""PKG-017 externally managed environments (PEP 668)."""

from __future__ import annotations

import pathlib

# Modeled marker without changing host installation.
# System Python may have /usr/lib/python3.14/EXTERNALLY-MANAGED or
# <venv>/pyvenv.cfg variant. We create a local marker file to test installer response.

MARKER_CONTENT = """[externally-managed]
Error=This environment is externally managed
; To install Python packages system-wide, try apt, et cetera
"""

# A file named EXTERNALLY-MANAGED at sysconfig scheme path would cause pip
# to refuse `pip install --break-system-packages` unless override given.
# Virtual environments are exempt per PEP 668.

MODELED_MARKER = pathlib.Path(__file__).parents[1] / "docs" / "EXTERNALLY-MANAGED.example"


def write_modeled_marker() -> pathlib.Path:
    MODELED_MARKER.parent.mkdir(parents=True, exist_ok=True)
    MODELED_MARKER.write_text(MARKER_CONTENT, encoding="utf-8")
    return MODELED_MARKER


def installer_response_note() -> str:
    return "pip install without --break-system-packages on externally-managed host would error; venv is exempt"


def override_policy_note() -> str:
    return "--break-system-packages overrides PEP 668 marker; distribution guidance discourages system pip"
