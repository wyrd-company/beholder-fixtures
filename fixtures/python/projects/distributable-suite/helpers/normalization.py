"""PKG-001 normalization helper: hyphen, underscore, dot -> canonical."""

try:
    from packaging.utils import canonicalize_name

    VARIANTS = {
        "hyphen": "distributable-suite-core",
        "underscore": "distributable_suite-extra",
        "dot": "distributable.suite.another",
    }

    CANONICAL = {k: canonicalize_name(v) for k, v in VARIANTS.items()}

    # Each spelling normalizes underscores/dots to hyphens per PEP 503
    assert CANONICAL["hyphen"] == "distributable-suite-core"
    assert CANONICAL["underscore"] == "distributable-suite-extra"
    assert CANONICAL["dot"] == "distributable-suite-another"

except ImportError:
    VARIANTS = {}
    CANONICAL = {}


def import_identity_map() -> dict:
    """Distribution -> import names."""
    return {
        "distributable-suite-core": ["suite_core", "suite_core_utils", "suite_shared_ns", "suite_standalone"],
        "distributable_suite-extra": ["suite_extra_underscore"],
        "distributable.suite.another": ["suite_extra_dot"],
    }
