/// DART-CAN-FLOW-004: pattern contexts and scope.
library;

/// A local pattern-variable declaration: destructures a record into two new
/// locals. (Pattern-variable declarations are local-only; Dart does not
/// permit them at library or class scope.)
String describeDeclarationContext() {
  final (a, b) = (2 + 3, 2 * 3);
  return 'a=$a b=$b';
}

/// An assignment context: the pattern's targets (`x`, `y`) already exist as
/// locals, so the pattern only assigns, it does not declare.
String describeAssignmentContext() {
  int x = 0;
  int y = 0;
  (x, y) = (5, 10);
  return 'x=$x y=$y';
}

/// An `if-case` context: the pattern either matches and binds, or the
/// branch is skipped.
String describeIfCaseContext(Object? value) {
  if (value case [int a, int b]) {
    return 'matched:$a,$b';
  }
  return 'no-match';
}

/// A switch context: the same pattern grammar, matched against every case in
/// turn.
String describeSwitchContext(Object? value) {
  return switch (value) {
    [int a, int b] => 'matched:$a,$b',
    _ => 'no-match',
  };
}

/// A `for` destructuring context: each loop iteration destructures one
/// element of the iterable through a record pattern.
List<int> describeForDestructuringContext(List<(int, int)> points) {
  final sums = <int>[];
  for (final (x, y) in points) {
    sums.add(x + y);
  }
  return sums;
}

/// Guard scope: the pattern's bindings (`a`, `b`) are visible inside the
/// `when` guard expression that follows them.
String describeGuardScope(Object? value) {
  return switch (value) {
    (int a, int b) when a > b => 'a-bigger:$a>$b',
    (int a, int b) => 'not-bigger:$a,$b',
    _ => 'other',
  };
}

/// Branch scope: each case introduces its own, independent binding named
/// `x`; the two `x` bindings below do not conflict because each is scoped to
/// its own branch.
String describeBranchScope(Object? value) {
  return switch (value) {
    int x => 'int-branch:$x',
    String x => 'string-branch:$x',
    _ => 'other',
  };
}

/// A closure defined within a matched branch captures that branch's
/// pattern-bound variable.
String describeClosureCapturingBinding(Object? value) {
  if (value case final int n) {
    int addN(int x) => x + n;
    return 'result=${addN(10)}';
  }
  return 'no-match';
}

/// Per-iteration bindings: a `for` destructuring context creates a fresh
/// binding on every iteration, so closures created in different iterations
/// each keep their own captured value rather than sharing one mutable slot.
List<String> describePerIterationBindings(List<(int, int)> points) {
  final closures = <String Function()>[];
  for (final (x, y) in points) {
    closures.add(() => '$x,$y');
  }
  return closures.map((closure) => closure()).toList();
}

List<String> describePatternContextsAndScope() {
  return <String>[
    'declarationContext=${describeDeclarationContext()}',
    'assignmentContext=${describeAssignmentContext()}',
    'ifCaseContext(match)=${describeIfCaseContext(const <int>[1, 2])}',
    'ifCaseContext(no-match)=${describeIfCaseContext('nope')}',
    'switchContext(match)=${describeSwitchContext(const <int>[3, 4])}',
    'forDestructuringContext=${describeForDestructuringContext(const <(int, int)>[(1, 2), (3, 4)])}',
    'guardScope(bigger)=${describeGuardScope((5, 2))}',
    'guardScope(not-bigger)=${describeGuardScope((2, 5))}',
    'branchScope(int)=${describeBranchScope(9)}',
    'branchScope(string)=${describeBranchScope('nine')}',
    'closureCapturingBinding=${describeClosureCapturingBinding(3)}',
    'perIterationBindings=${describePerIterationBindings(const <(int, int)>[(1, 1), (2, 2), (3, 3)])}',
  ];
}
