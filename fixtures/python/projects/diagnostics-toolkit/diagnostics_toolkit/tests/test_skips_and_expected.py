"""Skips and expected failures (PY-CAN-DIAG-009)."""

from __future__ import annotations

import sys
import unittest


class TestSkips(unittest.TestCase):
    """Exercises skip variants."""

    @unittest.skip("demonstration skip")
    def test_skipped_always(self) -> None:
        self.fail("should be skipped")

    @unittest.skipIf(sys.version_info < (3, 11), "requires 3.11+")
    def test_skip_if_false(self) -> None:
        # Condition false on 3.14, so this runs.
        self.assertTrue(True)

    @unittest.skipUnless(sys.platform.startswith("linux"), "linux only")
    def test_skip_unless(self) -> None:
        self.assertTrue(True)

    def test_skip_via_method(self) -> None:
        self.skipTest("skip via skipTest call")

    @unittest.skip("another skip")
    def test_another_skip(self) -> None:
        pass


class TestExpectedFailures(unittest.TestCase):
    """Exercises expectedFailure."""

    @unittest.expectedFailure
    def test_expected_failure(self) -> None:
        self.assertEqual(1, 2)

    @unittest.expectedFailure
    def test_expected_failure_with_exception(self) -> None:
        raise RuntimeError("expected")

    def test_unexpected_success_is_failure(self) -> None:
        # This test is NOT marked expectedFailure, so it passes normally.
        self.assertTrue(True)
