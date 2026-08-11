"""Subtests (PY-CAN-DIAG-009)."""

from __future__ import annotations

import unittest


class TestSubtests(unittest.TestCase):
    """Exercises unittest subtests."""

    def test_with_subtest_loop(self) -> None:
        for i in range(3):
            with self.subTest(i=i):
                self.assertGreaterEqual(i, 0)

    def test_subtest_with_messages(self) -> None:
        data = [(1, 2, 3), (2, 2, 4), (3, 5, 8)]
        for a, b, expected in data:
            with self.subTest(a=a, b=b):
                self.assertEqual(a + b, expected)

    def test_nested_subtests(self) -> None:
        for x in [1, 2]:
            with self.subTest(x=x):
                for y in [10, 20]:
                    with self.subTest(y=y):
                        self.assertIsInstance(x + y, int)
