"""Load failure discovery variant (PY-CAN-DIAG-009)."""

from __future__ import annotations

import unittest


class TestLoadFailureDiscovery(unittest.TestCase):
    """Programmatically discovers a broken test file and asserts load errors are captured."""

    def test_load_failure_is_captured(self) -> None:
        loader = unittest.TestLoader()
        # Discover the broken fixture directory; file fails to import.
        suite = loader.discover("diagnostics_toolkit/tests/broken_fixture", pattern="load_*.py")
        from io import StringIO

        stream = StringIO()
        result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
        output = stream.getvalue()
        # The broken file should cause an error entry; discovery attempted.
        total = result.testsRun + len(result.errors) + len(result.failures)
        self.assertGreaterEqual(total, 1)
        # Also verify that the broken fixture indeed fails on import directly.
        with self.assertRaises((ImportError, ModuleNotFoundError, RuntimeError, Exception)):
            import diagnostics_toolkit.tests.broken_fixture.load_failure_fixture  # type: ignore[import]
