/// Small self-check helpers shared by the fixture's executable entry
/// points. They compare an actual value against what each
/// demonstration is expected to produce and fail loudly on a mismatch,
/// since this project plans no separate test source.
library;

import 'dart:io';

/// Fails the process with [label] and [detail] on stderr.
Never fail(String label, String detail) {
  stderr.writeln('FAILED $label: $detail');
  exit(1);
}

/// Fails unless [actual] equals [expected].
void expectEqual(Object? actual, Object? expected, String label) {
  if (actual != expected) {
    fail(label, 'expected=$expected actual=$actual');
  }
}

/// Fails unless [actual] and [expected] contain the same elements in the
/// same order.
void expectList(List<Object?> actual, List<Object?> expected, String label) {
  final matches =
      actual.length == expected.length &&
      Iterable<int>.generate(
        actual.length,
      ).every((i) => actual[i] == expected[i]);
  if (!matches) {
    fail(label, 'expected=$expected actual=$actual');
  }
}
