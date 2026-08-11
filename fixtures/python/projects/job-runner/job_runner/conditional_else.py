"""Conditional and loop else (PY-CAN-FLOW-001)."""

from __future__ import annotations

# Correct else attachment: else binds to innermost loop, not to if.

def exhausted_for_else(items: list[int]) -> str:
    """For loop that exhausts without break triggers else."""
    for value in items:
        if value < 0:
            break
    else:
        return "exhausted"
    return "broken"


def terminated_for_else(items: list[int]) -> str:
    """For loop terminated by break skips else."""
    for value in items:
        if value == 2:
            break
    else:
        return "exhausted"
    return "terminated-by-break"


def exhausted_while_else(limit: int) -> str:
    """While loop that exhausts condition triggers else."""
    count = 0
    while count < limit:
        count += 1
    else:
        return "while-exhausted"
    return "unreachable"


def terminated_while_else(limit: int) -> str:
    """While loop terminated by break skips else."""
    count = 0
    while count < limit:
        if count == 1:
            break
        count += 1
    else:
        return "while-exhausted"
    return "while-broken"


def nested_loop_else_attachment(matrix: list[list[int]]) -> list[str]:
    """Demonstrate else binds to inner loop in nested structure."""
    results: list[str] = []
    for row in matrix:
        for value in row:
            if value == 99:
                break
        else:
            results.append("inner-exhausted")
            continue
        results.append("inner-broken")
        break
    else:
        results.append("outer-exhausted")
    return results


def return_prevents_else(items: list[int]) -> str:
    """Return inside loop prevents else execution."""

    def _inner() -> str:
        for value in items:
            if value == 1:
                return "returned"
        else:
            return "else-after-return-check"
        return "after-loop"

    return _inner()


def exception_prevents_else(items: list[int]) -> str:
    """Exception inside loop prevents else when not handled inside loop."""
    try:
        for value in items:
            if value == 99:
                raise ValueError("job-failed")
        else:
            return "exhausted-without-exception"
    except ValueError:
        return "handled-after-loop"
    return "unreachable"


def continue_through_finally(items: list[int]) -> list[str]:
    """Continue in try must still execute finally before next iteration."""
    log: list[str] = []
    for value in items:
        try:
            if value % 2 == 0:
                continue
            log.append(f"processed-{value}")
        finally:
            log.append(f"finally-{value}")
    else:
        log.append("loop-else")
    return log


def iterator_non_stop_failure() -> str:
    """Iterator raising non-StopIteration bypasses else."""

    class FlakyIterator:
        def __init__(self) -> None:
            self.step = 0

        def __iter__(self) -> FlakyIterator:
            return self

        def __next__(self) -> int:
            self.step += 1
            if self.step == 2:
                raise RuntimeError("mid-iteration failure")
            if self.step > 3:
                raise StopIteration
            return self.step

    try:
        for _ in FlakyIterator():
            pass
        else:
            return "else-ran"
    except RuntimeError:
        return "non-stop-failure"


def constant_reachability(flag: bool) -> str:
    """Constant condition shows else reachability is structural, not value-based."""
    # Structural: else belongs to loop, not to if.
    items = [1, 2, 3]
    for value in items:
        if True:  # constant true — optimizer may note but loop else unchanged
            if value == 10:
                break
        else:
            # This else belongs to the inner if, not the loop.
            pass
    else:
        return "outer-else-reachable"

    # While True with break makes else unreachable structurally.
    while True:
        break
    else:
        return "unreachable-while-else"

    # While False body never runs but else still executes (exhaustion).
    while False:
        pass
    else:
        return "while-false-else-executed"

    return "done"
