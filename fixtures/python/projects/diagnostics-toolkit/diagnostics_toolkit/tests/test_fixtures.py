"""Fixtures and cleanups (PY-CAN-DIAG-009)."""

from __future__ import annotations

import unittest


class TestFixturesAndCleanups(unittest.TestCase):
    """Exercises setUp/tearDown, setUpClass/tearDownClass, addCleanup, addClassCleanup."""

    @classmethod
    def setUpClass(cls) -> None:  # noqa: N802
        cls.shared_resource = {"value": 1}
        cls.addClassCleanup(cls._class_cleanup)

    @classmethod
    def _class_cleanup(cls) -> None:
        cls.shared_resource.clear()

    @classmethod
    def tearDownClass(cls) -> None:  # noqa: N802
        pass

    def setUp(self) -> None:  # noqa: N802
        self.per_test = []
        self.addCleanup(self._per_test_cleanup)
        self.per_test.append("setup")

    def _per_test_cleanup(self) -> None:
        self.per_test.clear()

    def tearDown(self) -> None:  # noqa: N802
        pass

    def test_with_fixture(self) -> None:
        self.assertIn("setup", self.per_test)
        self.assertEqual(self.shared_resource["value"], 1)

    def test_second_with_fixture(self) -> None:
        self.per_test.append("extra")
        self.assertEqual(len(self.per_test), 2)

    def test_partial_setup_cleanup(self) -> None:
        # Demonstrate that addCleanup runs even if test fails partway.
        self.addCleanup(lambda: self.per_test.append("cleanup-ran"))
        self.assertTrue(True)
