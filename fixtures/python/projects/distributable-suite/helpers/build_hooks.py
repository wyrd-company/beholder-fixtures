"""PKG-018 build hooks and config settings."""

from __future__ import annotations

# setuptools.build_meta hooks exercised via pip isolated build:
# - get_requires_for_build_wheel (returns [] as no setup_requires)
# - prepare_metadata_for_build_wheel
# - build_wheel
# - get_requires_for_build_sdist
# - build_sdist
# - get_requires_for_build_editable / prepare_metadata_for_build_editable / build_editable
#
# These hooks are optional per PEP 517; skipped hooks use fallback.
# Deterministic config setting example:
#   pip wheel --config-settings="--global-option=build_ext" is deprecated;
#   namespaced form is --config-settings=setuptools.build_meta:foo=bar
# We demonstrate a namespaced setting that is observable in build log.

CONFIG_SETTING_EXAMPLE = "--config-settings=setuptools.build_meta:coerce-build-tag=1"

HOOK_SEQUENCE = [
    "get_requires_for_build_wheel",
    "prepare_metadata_for_build_wheel",
    "build_wheel",
    "get_requires_for_build_sdist",
    "build_sdist",
]

# Hook selection: pip calls prepare_metadata then build_wheel; prepared metadata must match final.
# Subprocess assumption invalid: hooks run in isolated subprocess, not same process as pip.

EMPTY_REQUIRES_CLAIM = "setuptools.build_meta 84.0.0 get_requires_for_build_* returns [] when no setup_requires (lines 265-310, 435-438)"


def config_settings_demo() -> dict:
    return {
        "setting": CONFIG_SETTING_EXAMPLE,
        "namespace": "setuptools.build_meta",
        "deterministic": "same setting yields same wheel metadata",
        "backend_spelling": "tool.setuptools vs --config-settings namespace",
    }
