"""Doctest execution coverage (PY-CAN-DIAG-014)."""

from __future__ import annotations

import doctest
import pathlib
import unittest


def load_tests(loader: unittest.TestLoader, tests: unittest.TestSuite, pattern: object) -> unittest.TestSuite:  # noqa: N802
    """Hook for unittest discover to add doctests."""

    # Docstring examples from the module.
    tests.addTests(doctest.DocTestSuite("diagnostics_toolkit.doctest_examples"))
    # Text-file examples.
    txt_path = pathlib.Path(__file__).parent.parent / "doctest_text.txt"
    if txt_path.exists():
        tests.addTests(
            doctest.DocFileSuite(
                str(txt_path),
                module_relative=False,
                optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE,
            )
        )
    return tests


class TestDoctestDirect(unittest.TestCase):
    """Direct doctest execution verifies shared state, exception, and option directive."""

    def test_module_doctests(self) -> None:
        import diagnostics_toolkit.doctest_examples as mod

        failure_count, test_count = doctest.testmod(mod, optionflags=doctest.ELLIPSIS, verbose=False)
        self.assertEqual(failure_count, 0)
        self.assertGreater(test_count, 0)

    def test_text_file_doctests(self) -> None:
        txt_path = pathlib.Path(__file__).parent.parent / "doctest_text.txt"
        failure_count, test_count = doctest.testfile(
            str(txt_path),
            module_relative=False,
            optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE,
            verbose=False,
        )
        self.assertEqual(failure_count, 0)
        self.assertGreater(test_count, 0)
