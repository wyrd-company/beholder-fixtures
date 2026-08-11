"""PKG-001 normalization helper: hyphen, underscore, dot -> canonical.

Canonicalization follows PEP 503 name normalization directly so the demonstration
executes in the default runtime context without requiring the third-party
``packaging`` distribution (which is not part of this fixture's declared runtime).
"""

from __future__ import annotations

import re

# Runs of dash, underscore, or dot collapse to a single dash and the name is
# lowercased. This is the PEP 503 normalized-name rule that pip and installers
# use to compare distribution names across their hyphen/underscore/dot spellings.
_SEPARATOR_RUN = re.compile(r"[-_.]+")


def canonicalize_name(name: str) -> str:
    """Return the PEP 503 canonical form of a distribution name."""
    return _SEPARATOR_RUN.sub("-", name).lower()


VARIANTS = {
    "hyphen": "distributable-suite-core",
    "underscore": "distributable_suite-extra",
    "dot": "distributable.suite.another",
}

CANONICAL = {key: canonicalize_name(value) for key, value in VARIANTS.items()}

# Each spelling normalizes underscores/dots to hyphens per PEP 503.
assert CANONICAL["hyphen"] == "distributable-suite-core"
assert CANONICAL["underscore"] == "distributable-suite-extra"
assert CANONICAL["dot"] == "distributable-suite-another"


def import_identity_map() -> dict:
    """Distribution -> import names."""
    return {
        "distributable-suite-core": ["suite_core", "suite_core_utils", "suite_shared_ns", "suite_standalone"],
        "distributable_suite-extra": ["suite_extra_underscore"],
        "distributable.suite.another": ["suite_extra_dot"],
    }
