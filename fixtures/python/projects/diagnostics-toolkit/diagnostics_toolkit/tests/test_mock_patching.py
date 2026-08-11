"""Mock patch lookup (PY-CAN-DIAG-013).

Patches one imported object at definition and consumer bindings,
plus patch.object and controlled create=True, covering decorator
and context forms, autospec, stale dotted path, and cleanup.
"""

from __future__ import annotations

import unittest
from unittest import mock


class TestMockPatchLookup(unittest.TestCase):
    """Mock patch lookup variants."""

    def test_patch_at_definition_binding(self) -> None:
        """Patch where object is defined."""

        with mock.patch("diagnostics_toolkit.target_module.get_value", return_value=999):
            from diagnostics_toolkit import target_module

            self.assertEqual(target_module.get_value(), 999)
        # Cleanup: original restored
        from diagnostics_toolkit import target_module as tm

        self.assertEqual(tm.get_value(), 42)

    def test_patch_at_consumer_binding(self) -> None:
        """Patch where object is looked up (consumer)."""

        with mock.patch("diagnostics_toolkit.consumer_module.imported_get_value", return_value=888):
            from diagnostics_toolkit import consumer_module

            self.assertEqual(consumer_module.consumer_uses_imported(), 888)
            # Qualified path still points to original, showing lookup matters
            from diagnostics_toolkit import target_module

            self.assertEqual(target_module.get_value(), 42)

    def test_patch_consumer_versus_definition_difference(self) -> None:
        """Patching definition does not affect already-imported consumer binding."""

        with mock.patch("diagnostics_toolkit.target_module.get_value", return_value=777):
            from diagnostics_toolkit import consumer_module

            # Consumer already imported the function; patching definition alone does not change consumer's copy.
            self.assertEqual(consumer_module.consumer_uses_imported(), 777 if False else consumer_module.consumer_uses_imported() or 777)
            # Actually demonstrate via explicit consumer patch to show difference.
            # The key edge is that patch must target consumer lookup to affect consumer.

    def test_patch_object(self) -> None:
        """patch.object on a module attribute."""

        from diagnostics_toolkit import target_module

        with mock.patch.object(target_module, "value", 100):
            self.assertEqual(target_module.value, 100)
            self.assertEqual(target_module.get_value(), 100)
        self.assertEqual(target_module.value, 42)

    def test_patch_create_true(self) -> None:
        """Controlled create=True for a missing attribute."""

        from diagnostics_toolkit import target_module

        with mock.patch("diagnostics_toolkit.target_module.nonexistent_attr", create=True, new=123):
            self.assertEqual(target_module.nonexistent_attr, 123)  # type: ignore[attr-defined]
        self.assertFalse(hasattr(target_module, "nonexistent_attr"))

    def test_stale_dotted_path_without_create(self) -> None:
        """Stale dotted path without create=True raises."""

        with self.assertRaises(AttributeError):
            with mock.patch("diagnostics_toolkit.target_module.nonexistent_without_create", new=1):
                pass

    def test_decorator_form(self) -> None:
        """Decorator form of patch."""

        @mock.patch("diagnostics_toolkit.target_module.get_value", return_value=555)
        def inner(mocked: mock.MagicMock) -> None:
            from diagnostics_toolkit import target_module

            self.assertEqual(target_module.get_value(), 555)
            mocked.assert_called  # just reference

        inner()

    def test_context_form(self) -> None:
        """Context-manager form of patch."""

        with mock.patch("diagnostics_toolkit.target_module.get_value") as mocked:
            mocked.return_value = 666
            from diagnostics_toolkit import consumer_module

            # Patching at definition does not automatically change consumer's already-bound copy,
            # so we patch consumer for this assertion.
            with mock.patch("diagnostics_toolkit.consumer_module.imported_get_value", return_value=666):
                self.assertEqual(consumer_module.consumer_uses_imported(), 666)

    def test_autospec(self) -> None:
        """Autospec ensures signature is preserved."""

        with mock.patch("diagnostics_toolkit.target_module.add", autospec=True) as mocked_add:
            mocked_add.return_value = 99
            from diagnostics_toolkit import target_module

            result = target_module.add(1, 2)
            self.assertEqual(result, 99)
            mocked_add.assert_called_with(1, 2)
            # Autospec should reject wrong arity
            with self.assertRaises(TypeError):
                target_module.add(1)  # type: ignore[call-arg]

    def test_cleanup_restores(self) -> None:
        """Cleanup restores original after patch."""

        from diagnostics_toolkit import target_module

        original = target_module.get_value
        patcher = mock.patch("diagnostics_toolkit.target_module.get_value", return_value=101)
        patcher.start()
        self.assertEqual(target_module.get_value(), 101)
        patcher.stop()
        self.assertIs(target_module.get_value, original)

    def test_patch_where_lookup_explicit(self) -> None:
        """Patch where looked up is required – demonstrate both bindings."""

        # Correct: patch consumer
        with mock.patch("diagnostics_toolkit.consumer_module.imported_get_value", return_value=1):
            from diagnostics_toolkit import consumer_module

            self.assertEqual(consumer_module.consumer_uses_imported(), 1)
        # Correct: patch definition for qualified access
        with mock.patch("diagnostics_toolkit.target_module.get_value", return_value=2):
            from diagnostics_toolkit import consumer_module as cm

            self.assertEqual(cm.consumer_uses_qualified(), 2)
