"""Discovered module/class/method tests (PY-CAN-DIAG-009)."""

from __future__ import annotations

import unittest


def setUpModule() -> None:  # noqa: N802
    pass


def tearDownModule() -> None:  # noqa: N802
    pass


class TestBasicDiscovery(unittest.TestCase):
    """Basic discovered test class."""

    def test_alpha(self) -> None:
        self.assertEqual(1 + 1, 2)

    def test_beta(self) -> None:
        self.assertTrue("hello".upper() == "HELLO")

    def test_gamma_with_assert(self) -> None:
        self.assertIn("a", "abc")


class TestSecondDiscovery(unittest.TestCase):
    """Second discovered class in same module."""

    def test_one(self) -> None:
        self.assertIsNotNone(object())

    def test_two(self) -> None:
        self.assertGreater(5, 3)
