"""Inherited tests (PY-CAN-DIAG-009)."""

from __future__ import annotations

import unittest


class BaseDiscoverable(unittest.TestCase):
    """Base class with a test that should be inherited."""

    def test_inherited_generic(self) -> None:
        self.assertTrue(True)

    def test_inherited_math(self) -> None:
        self.assertEqual(2 * 3, 6)


class DerivedDiscoverable(BaseDiscoverable):
    """Derived class inherits tests from base."""

    def test_derived_specific(self) -> None:
        self.assertEqual("foo" + "bar", "foobar")


class AnotherDerived(BaseDiscoverable):
    """Another derived to show multiple inheritors."""

    def test_another_specific(self) -> None:
        self.assertIsInstance([], list)
