"""Conditional definitions and definition order (PY-CAN-FLOW-013)."""

from __future__ import annotations

import sys

# Define same public name differently by version/platform/availability.

if sys.version_info >= (3, 11):
    job_policy = "policy-modern"
    JobPolicy = dict[str, str]
else:
    job_policy = "policy-legacy"
    JobPolicy = dict

# Platform-gated definition: Linux is the local platform; Windows branch is
# present as valid source but never executed locally.
if sys.platform.startswith("linux"):
    platform_label = "linux"
else:
    platform_label = "other"

# Availability-gated definition via optional dependency probe.
try:
    import multiprocessing as _mp  # noqa: F401  # availability probe

    concurrency_backend = "multiprocessing-available"
except ImportError:
    concurrency_backend = "multiprocessing-unavailable"

# Later redefinition: same public name rebound after first binding.
job_retries = 3
# ... later in module execution, redefined based on derived state
job_retries = 5

# Unexecuted branch: parser accepts both branches even though one never runs.
if False:
    unexecuted_value = "never-bound-at-runtime"
else:
    unexecuted_value = "taken-branch"


def use_after_binding() -> dict[str, object]:
    """Use names only after execution has bound them."""
    return {
        "job_policy": job_policy,
        "platform_label": platform_label,
        "concurrency_backend": concurrency_backend,
        "job_retries": job_retries,
        "unexecuted_value": unexecuted_value,
    }


# Import-time reference before definition would be NameError; guard by defining first.
# Demonstrate that reference before binding is invalid, so we defer use to function.
def deferred_reference_demo(flag: bool) -> str:
    if flag:
        late_value = "late-bound"
    else:
        late_value = "alternative"
    return late_value


# Separate-file syntax gating note: all live files parse under selected interpreter.
def syntax_gating_note() -> str:
    return "all-live-files-parse-under-3.14"


# Version-gated alternative implementation — same public API, different binding.
if sys.version_info >= (3, 11):
    def retry_strategy(attempt: int) -> str:
        return f"modern-retry-{attempt}"
else:
    def retry_strategy(attempt: int) -> str:  # noqa: F811 — redefinition is the point
        return f"legacy-retry-{attempt}"
