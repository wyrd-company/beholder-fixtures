"""Test-runner main-identity variant of PY-CAN-INT-007 (standard-library unittest)."""

from __future__ import annotations

import multiprocessing
import pickle
import sys
import unittest

from feature_integration_suite.mp_workers import worker


class TestRunnerMainIdentity(unittest.TestCase):
    """Verify multiprocessing spawn works when test runner is __main__, without recursive startup."""

    def test_worker_pickle_identity_under_test_runner(self) -> None:
        # When run via `python -m unittest`, __main__ is unittest.__main__, not mp_workers
        # Worker must be importable by its canonical module name, not __main__
        self.assertEqual(worker.__module__, "feature_integration_suite.mp_workers")
        data = pickle.dumps(worker)
        restored = pickle.loads(data)
        self.assertIs(restored, worker)
        self.assertEqual(restored(6), 36)

    def test_spawn_without_recursive_startup(self) -> None:
        # Spawn a child via spawn context; child imports worker by module name, not via test's __main__
        ctx = multiprocessing.get_context("spawn")
        with ctx.Pool(1) as pool:
            result = pool.apply(worker, (9,))
        self.assertEqual(result, 81)

    def test_spawn_fork_if_available(self) -> None:
        try:
            ctx = multiprocessing.get_context("fork")
        except ValueError:
            self.skipTest("fork not available")
        with ctx.Pool(1) as pool:
            result = pool.apply(worker, (4,))
        self.assertEqual(result, 16)

    def test_local_function_not_spawnable(self) -> None:
        def local(y: int) -> int:
            return y + 1

        with self.assertRaises((AttributeError, pickle.PicklingError)):
            pickle.dumps(local)
            # Also try spawn path: local cannot be pickled for child
            ctx = multiprocessing.get_context("spawn")
            with ctx.Pool(1) as pool:
                pool.apply(local, (1,))

    def test_main_is_test_runner_not_worker_module(self) -> None:
        # Demonstrate that __main__ under unittest is not the worker module
        self.assertNotEqual(sys.modules["__main__"].__name__, "feature_integration_suite.mp_workers")
        # But worker remains importable via its distribution name
        import importlib

        mod = importlib.import_module("feature_integration_suite.mp_workers")
        self.assertIs(mod.worker, worker)
