/// DART-CAN-FLOW-001: statements, loops, labels, and reachability.
library;

/// A `Never`-typed function: it always throws, so callers know code after a
/// call to it is unreachable.
Never explode(String message) => throw StateError(message);

/// A classic C-style `for` loop with a plain `break`.
List<int> describeForLoop() {
  final results = <int>[];
  for (var i = 0; i < 5; i++) {
    if (i == 3) {
      break;
    }
    results.add(i);
  }
  return results;
}

/// A `while` loop with a plain `continue`.
List<int> describeWhileLoop() {
  final results = <int>[];
  var i = 0;
  while (i < 5) {
    if (i == 2) {
      i += 1;
      continue;
    }
    results.add(i);
    i += 1;
  }
  return results;
}

/// A `do`-`while` loop, which always runs its body at least once.
List<int> describeDoWhileLoop() {
  final results = <int>[];
  var i = 0;
  do {
    results.add(i);
    i += 1;
  } while (i < 3);
  return results;
}

/// A `for`-in loop over an `Iterable`.
List<int> describeForInLoop() {
  final results = <int>[];
  for (final value in <int>[10, 20, 30]) {
    results.add(value);
  }
  return results;
}

/// Nested labels: a labeled outer loop, targeted by both a labeled
/// `continue` and a labeled `break` from within the inner loop.
List<String> describeNestedLabels() {
  final results = <String>[];
  outer:
  for (var i = 0; i < 3; i++) {
    for (var j = 0; j < 3; j++) {
      if (j == 1) {
        continue outer;
      }
      if (i == 2) {
        break outer;
      }
      results.add('$i-$j');
    }
  }
  return results;
}

/// A labeled block statement, exited early with a labeled `break`.
String describeLabeledBlockBreak(int value) {
  String result;
  block:
  {
    if (value < 0) {
      result = 'negative';
      break block;
    }
    result = 'non-negative';
  }
  return result;
}

/// `return` and `throw` as statement forms; the `throw` branch never falls
/// through to the `return` below it.
int describeReturnOrThrow(bool shouldThrow) {
  if (shouldThrow) {
    throw ArgumentError('shouldThrow was true');
  }
  return 1;
}

/// A call to a `Never`-returning function makes the statements after the
/// call (within the same branch) unreachable; the outer function remains
/// reachable through the branch that does not call it.
String describeNeverCall(bool trigger) {
  if (trigger) {
    explode('triggered');
  }
  return 'safe';
}

/// A continue-to-switch label: `continue label1;` jumps to the case labeled
/// `label1`, Dart's explicit alternative to implicit case fall-through.
String describeContinueToSwitchLabel(int value) {
  switch (value) {
    case 0:
      continue zeroOrOne;
    zeroOrOne:
    case 1:
      return 'zero-or-one';
    default:
      return 'other';
  }
}

List<String> describeStatementsLoopsAndReachability() {
  return <String>[
    'forLoop=${describeForLoop()}',
    'whileLoop=${describeWhileLoop()}',
    'doWhileLoop=${describeDoWhileLoop()}',
    'forInLoop=${describeForInLoop()}',
    'nestedLabels=${describeNestedLabels()}',
    'labeledBlockBreak(negative)=${describeLabeledBlockBreak(-1)}',
    'labeledBlockBreak(non-negative)=${describeLabeledBlockBreak(1)}',
    'returnOrThrow(false)=${describeReturnOrThrow(false)}',
    'neverCall(false)=${describeNeverCall(false)}',
    'continueToSwitchLabel(0)=${describeContinueToSwitchLabel(0)}',
    'continueToSwitchLabel(1)=${describeContinueToSwitchLabel(1)}',
    'continueToSwitchLabel(9)=${describeContinueToSwitchLabel(9)}',
  ];
}
