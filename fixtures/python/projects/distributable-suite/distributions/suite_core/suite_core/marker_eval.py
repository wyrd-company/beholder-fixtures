"""PKG-006 marker evaluation demonstration."""

from __future__ import annotations

import sys
import platform
from importlib.metadata import Distribution

MARKER_EXAMPLES = {
    "ordinary": "requests>=2.28.1",
    "python_version": "importlib-metadata; python_version < '3.11'",
    "platform": "pywin32; sys_platform == 'win32'",
    "platform_system": "typing-extensions; platform_system == 'Linux'",
    "implementation": "packaging; implementation_name == 'cpython'",
    "direct_reference": "certifi @ file:///tmp/local-certifi-placeholder",
    "boolean_composed": "urllib3; (python_version >= '3.10' and sys_platform == 'linux') or implementation_name == 'cpython'",
}

CONTRADICTORY_MARKER = "contradictory-pkg; python_version < '3.10' and python_version >= '3.12'"


def evaluate_markers() -> dict[str, bool]:
    """Evaluate markers via packaging.markers (standard)."""
    try:
        from packaging.markers import Marker
    except ImportError:
        return {k: False for k in MARKER_EXAMPLES}
    env = {
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}",
        "sys_platform": sys.platform,
        "platform_system": platform.system(),
        "implementation_name": "cpython",
    }
    result: dict[str, bool] = {}
    for key, req in MARKER_EXAMPLES.items():
        if ";" in req:
            _, marker_str = req.split(";", 1)
            result[key] = Marker(marker_str.strip()).evaluate()
        else:
            result[key] = True
    # contradictory
    marker_str = CONTRADICTORY_MARKER.split(";", 1)[1]
    result["contradictory"] = Marker(marker_str.strip()).evaluate()
    return result
