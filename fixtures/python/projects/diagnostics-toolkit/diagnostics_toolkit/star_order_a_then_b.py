"""Star-import order a-then-b (PY-CAN-DIAG-022).

Valid source declarations with ImportFrom star nodes for code-graph evaluation.
"""

from diagnostics_toolkit.star_a import *  # noqa: F403,F401
from diagnostics_toolkit.star_b import *  # noqa: F403,F401

# After both star imports, shared_name is "from-b" (b overwrites a).
ORDER = "a_then_b"
SHARED_AFTER_BOTH = shared_name  # type: ignore[name-defined]  # noqa: F405
UNIQUE_A_PRESENT = "unique_a" in dir()  # type: ignore
UNIQUE_B_PRESENT = "unique_b" in dir()  # type: ignore
