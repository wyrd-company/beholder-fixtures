/// Lexical capture, mutation of a captured variable observed after
/// capture, a recursive local closure, and per-iteration loop capture.
library;

/// Returns a closure that captures and mutates [start] by reference.
int Function() makeCounter(int start) {
  var count = start;
  return () {
    count += 1;
    return count;
  };
}

/// Demonstrates that a captured variable's later mutation is visible to
/// a closure created before the mutation: Dart closures capture the
/// variable itself, not a snapshot of its value at closure-creation
/// time.
List<int> mutateAfterCapture() {
  var value = 1;
  int Function() readValue = () => value;
  value = 41;
  return <int>[readValue(), value];
}

/// A recursive local closure computing a factorial. It is declared as a
/// named local function so that it can call itself by name.
int Function(int) makeFactorial() {
  int factorial(int n) => n <= 1 ? 1 : n * factorial(n - 1);
  return factorial;
}

/// Loop-iteration capture: Dart's `for` loop creates a fresh binding
/// for the loop variable on every iteration, so closures created in
/// different iterations capture distinct values rather than one shared
/// variable.
List<int Function()> captureEachIteration() {
  final closures = <int Function()>[];
  for (var i = 0; i < 3; i++) {
    closures.add(() => i);
  }
  return closures;
}
