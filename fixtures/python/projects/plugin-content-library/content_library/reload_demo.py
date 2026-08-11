"""Reload and stale references (PY-CAN-MOD-019)."""

from __future__ import annotations

import importlib
import pathlib
import sys


def reload_demo() -> dict[str, object]:
    import content_library.reload_target as target
    import content_library.reload_dep as dep

    old_module = target
    old_holder_cls = target.Holder
    old_instance = target.Holder()
    old_get_version = target.get_version
    old_old_name = getattr(target, "OLD_NAME", None)
    old_version = target.VERSION
    old_dep_value = dep.DEP_VALUE

    tmp_path = pathlib.Path(__file__).with_name("reload_target.py")
    dep_path = pathlib.Path(__file__).with_name("reload_dep.py")
    original_text = tmp_path.read_text(encoding="utf-8")
    original_dep_text = dep_path.read_text(encoding="utf-8")
    edited_text = original_text.replace("VERSION = 1", "VERSION = 2").replace('kind = "holder-v1"', 'kind = "holder-v2"').replace('OLD_NAME = "will-be-removed-after-edit"', '# OLD_NAME removed in v2')
    edited_dep_text = original_dep_text.replace('DEP_VALUE = "dep-v1"', 'DEP_VALUE = "dep-v2"')

    tmp_path.write_text(edited_text, encoding="utf-8")
    dep_path.write_text(edited_dep_text, encoding="utf-8")
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
        # Non-recursive dependency: reload_target's dependency was edited, but reloading target alone does NOT reload the dependency.
        dep_value_after = dep.DEP_VALUE
        reloaded_dep_value = reloaded.DEP_VALUE  # captured at reload time from reload_dep module (still v1)
        dep_not_recursive = dep_value_after == "dep-v1" and reloaded_dep_value == "dep-v1"
        # Extension reload variant: attempt to reload native extension.
        try:
            import content_library._native_ext as ext_mod

            ext_reloaded = importlib.reload(ext_mod)
            extension_reload_status = f"reloaded:{ext_reloaded.hello()}"  # type: ignore[attr-defined]
        except Exception as exc:
            extension_reload_status = f"extension-reload:{exc.__class__.__name__}: {exc}"
    finally:
        tmp_path.write_text(original_text, encoding="utf-8")
        dep_path.write_text(original_dep_text, encoding="utf-8")
        importlib.reload(target)
        importlib.reload(dep)

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
        "dependency_not_recursive": dep_not_recursive,
        "dep_value_still_v1": dep_value_after,
        "extension_reload": extension_reload_status,
        "not_thread_safe": "reload is not thread-safe",
        "source_state_selection": "reloaded source comes from current file content at reload time",
    }


def extension_reload_demo() -> dict[str, object]:
    """Dedicated extension reload path (PY-CAN-MOD-019)."""
    import importlib

    try:
        import content_library._native_ext as ext_mod

        before = ext_mod.hello()  # type: ignore[attr-defined]
        reloaded = importlib.reload(ext_mod)
        after = reloaded.hello()  # type: ignore[attr-defined]
        return {"before": before, "after": after, "reloaded": True}
    except Exception as exc:
        return {"error": str(exc), "type": exc.__class__.__name__}


def dependency_not_recursive_demo() -> dict[str, object]:
    """Dependency reload is not recursive."""
    import importlib
    import content_library.reload_target as target
    import content_library.reload_dep as dep

    dep_before = dep.DEP_VALUE
    # Edit dep file, reload only target, observe dep unchanged.
    dep_path = pathlib.Path(__file__).with_name("reload_dep.py")
    original = dep_path.read_text(encoding="utf-8")
    edited = original.replace('DEP_VALUE = "dep-v1"', 'DEP_VALUE = "dep-v2"')
    dep_path.write_text(edited, encoding="utf-8")
    try:
        importlib.reload(target)
        after = dep.DEP_VALUE
        return {"before": dep_before, "after": after, "not_recursive": after == dep_before}
    finally:
        dep_path.write_text(original, encoding="utf-8")
        importlib.reload(dep)
        importlib.reload(target)


def reload_dependencies_not_recursive_note() -> str:
    return "reload of a module does not reload modules it imports"
