"""Intentionally broken fixture to demonstrate discovery load failure (PY-CAN-DIAG-009)."""

import nonexistent_broken_module_xyz  # type: ignore[import]  # raises ModuleNotFoundError

import unittest


class TestShouldNotBeDiscovered(unittest.TestCase):
    def test_dummy(self) -> None:
        self.assertTrue(True)
