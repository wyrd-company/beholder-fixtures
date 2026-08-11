"""Reload and stale references (PY-CAN-MOD-019)."""

from __future__ import annotations

import importlib
import pathlib
import sys


def reload_demo() -> dict[str, object]:
    import content_library.reload_target as target

    old_module = target
    old_holder_cls = target.Holder
    old_instance = target.Holder()
    old_get_version = target.get_version
    old_old_name = getattr(target, "OLD_NAME", None)
    old_version = target.VERSION

    # Simulate source change by editing the file content before reload.
    # Instead of mutating tracked source, we monkey-patch the source used by
    # the loader: overwrite the module's attribute to new values, then
    # reload from a temporary edited file path.  For the fixture we demonstrate
    # the shape by directly mutating the file in a temp copy and reloading
    # via spec_from_file_location with a new loader state.
    # Simpler: reload after manually changing VERSION via file rewrite in a
    # temporary location that the spec will load.
    tmp_path = pathlib.Path(__file__).with_name("reload_target.py")
    original_text = tmp_path.read_text(encoding="utf-8")
    edited_text = original_text.replace("VERSION = 1", "VERSION = 2").replace('kind = "holder-v1"', 'kind = "holder-v2"').replace('OLD_NAME = "will-be-removed-after-edit"', '# OLD_NAME removed in v2')

    # Write edited version, reload, then restore original to keep tree clean.
    tmp_path.write_text(edited_text, encoding="utf-8")
    try:
        reloaded = importlib.reload(target)
        new_holder_cls = reloaded.Holder
        new_instance = reloaded.Holder()
        new_version = reloaded.VERSION
        has_old_name = hasattr(reloaded, "OLD_NAME")
        module_is_same = old_module is reloaded
        old_alias_still_v1 = old_holder_cls.kind == "holder-v1"
        new_class_is_v2 = new_holder_cls.kind == "holder-v2"
        old_instance_stale = old_instance.kind == "holder-v1"
        old_func_stale = old_get_version() == old_version
        new_func_updated = reloaded.get_version() == 2
    finally:
        tmp_path.write_text(original_text, encoding="utf-8")
        # Reload again to restore original state for subsequent imports.
        importlib.reload(target)

    # Note: functions close over the module's global dict, so an old
    # function alias sees the new VERSION after reload (not stale).  Old
    # class objects and instances remain stale, and removed names are
    # retained in the module dict (not deleted) — both are expected reload
    # semantics.
    return {
        "module_identity_preserved": module_is_same,
        "new_version": new_version,
        "old_alias_stale": old_alias_still_v1,
        "new_class_updated": new_class_is_v2,
        "old_instance_stale": old_instance_stale,
        "old_func_reflects_new": not old_func_stale,
        "new_func_updated": new_func_updated,
        "removed_name_retained_via_old_alias": old_old_name,
        "removed_name_retained_in_module": has_old_name,
        "not_thread_safe": "reload is not thread-safe",
        "extension_reload_note": "extension modules may not reload cleanly",
        "dependencies_not_recursive": "reload does not recursively reload dependencies",
        "source_state_selection": "reloaded source comes from current file content at reload time",
    }


def reload_dependencies_not_recursive_note() -> str:
    return "reload of a module does not reload modules it imports"
