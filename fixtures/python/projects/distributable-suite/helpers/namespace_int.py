"""PY-CAN-INT-004 namespace package split across distributions."""

from __future__ import annotations

import importlib.resources as res


def import_both_contributions():
    import suite_shared_ns.plugin_core as core
    import suite_shared_ns.plugin_src as src

    return core.get_value(), src.get_value()


def read_namespace_resources():
    # Aggregated resources from both distributions via namespace __path__
    files = res.files("suite_shared_ns")
    names = [p.name for p in files.iterdir()] if files.is_dir() else []
    core_data = res.files("suite_shared_ns").joinpath("data_core.txt").read_text(encoding="utf-8") if (res.files("suite_shared_ns").joinpath("data_core.txt").is_file()) else ""
    return names, core_data


def ownership_note() -> str:
    return "one package to many distributions: suite_shared_ns owned by distributable-suite-core and distributable-suite-src"


def editable_resource_note() -> str:
    return "editable installs compose namespace via .pth/finder; uninstall of one portion should not damage other's files"
