/// DART-CAN-FLOW-002: switch statements, expressions, and exhaustiveness.
library;

enum Signal { red, yellow, green }

sealed class Shape {}

class Circle extends Shape {
  final double radius;

  Circle(this.radius);
}

class SquareShape extends Shape {
  final double side;

  SquareShape(this.side);
}

/// A switch *statement* with constant cases.
String describeConstantSwitch(int value) {
  switch (value) {
    case 1:
      return 'one';
    case 2:
      return 'two';
    default:
      return 'other';
  }
}

/// A switch statement with pattern cases and guards (`when`).
String describeGuardedSwitch(int value) {
  switch (value) {
    case int n when n < 0:
      return 'negative';
    case int n when n == 0:
      return 'zero';
    case int n:
      return 'positive:$n';
  }
}

/// A switch *expression*, the value-producing form.
String describeSwitchExpression(int value) => switch (value) {
  0 => 'zero',
  1 => 'one',
  _ => 'many',
};

/// An enum scrutinee: exhaustive over every enum value, no `default` needed.
String describeEnumSwitch(Signal signal) => switch (signal) {
  Signal.red => 'stop',
  Signal.yellow => 'caution',
  Signal.green => 'go',
};

/// A `bool` scrutinee: exhaustive over both Boolean values.
String describeBoolSwitch(bool flag) => switch (flag) {
  true => 'yes',
  false => 'no',
};

/// A nullable scrutinee: an explicit `null` case alongside a present-value
/// case makes the switch exhaustive over `String?`.
String describeNullableSwitch(String? value) => switch (value) {
  null => 'absent',
  final v => 'present:$v',
};

/// A sealed-class scrutinee: exhaustive over every known subtype, no
/// `default` needed.
String describeSealedSwitch(Shape shape) => switch (shape) {
  Circle(radius: final r) => 'circle:$r',
  SquareShape(side: final s) => 'square:$s',
};

/// A record scrutinee, matched positionally.
String describeRecordSwitch((int, int) point) => switch (point) {
  (0, 0) => 'origin',
  (final x, 0) => 'on-x-axis:$x',
  (0, final y) => 'on-y-axis:$y',
  (final x, final y) => 'point:$x,$y',
};

/// Wildcard restoration: a positional `_` inside a record pattern discards
/// that component instead of binding it, and a bare `_` case restores
/// catch-all matching as the final arm.
String describeWildcardRestoration(Object? value) => switch (value) {
  (int _, int y) => 'second:$y',
  _ => 'unmatched',
};

/// Empty-case grouping: several constant cases share one body by leaving the
/// preceding cases empty (falling through to the next labeled case).
String describeEmptyCaseGrouping(int value) {
  switch (value) {
    case 1:
    case 2:
    case 3:
      return 'small';
    default:
      return 'other';
  }
}

/// A logical-or pattern collapses several constant alternatives into one
/// case.
String describeLogicalOrPattern(int value) {
  switch (value) {
    case 1 || 2 || 3:
      return 'small';
    case int n when n > 100:
      return 'large';
    default:
      return 'medium';
  }
}

/// A labeled `continue` inside a pattern-and-guard switch statement, jumping
/// from a guarded case to a later constant case's body.
String describeLabeledContinueToGuardedTarget(int value) {
  switch (value) {
    case int n when n < 0:
      continue nonPositive;
    nonPositive:
    case 0:
      return 'non-positive';
    default:
      return 'positive';
  }
}

List<String> describeSwitchFormsAndExhaustiveness() {
  return <String>[
    'constantSwitch(1)=${describeConstantSwitch(1)}',
    'constantSwitch(9)=${describeConstantSwitch(9)}',
    'guardedSwitch(-1)=${describeGuardedSwitch(-1)}',
    'guardedSwitch(0)=${describeGuardedSwitch(0)}',
    'guardedSwitch(5)=${describeGuardedSwitch(5)}',
    'switchExpression(0)=${describeSwitchExpression(0)}',
    'switchExpression(7)=${describeSwitchExpression(7)}',
    'enumSwitch=${describeEnumSwitch(Signal.yellow)}',
    'boolSwitch=${describeBoolSwitch(true)}',
    'nullableSwitch(null)=${describeNullableSwitch(null)}',
    'nullableSwitch(present)=${describeNullableSwitch('hi')}',
    'sealedSwitch(circle)=${describeSealedSwitch(Circle(2))}',
    'sealedSwitch(square)=${describeSealedSwitch(SquareShape(3))}',
    'recordSwitch(origin)=${describeRecordSwitch((0, 0))}',
    'recordSwitch(x-axis)=${describeRecordSwitch((4, 0))}',
    'recordSwitch(point)=${describeRecordSwitch((4, 5))}',
    'wildcardRestoration(match)=${describeWildcardRestoration((1, 2))}',
    'wildcardRestoration(unmatched)=${describeWildcardRestoration('nope')}',
    'emptyCaseGrouping(2)=${describeEmptyCaseGrouping(2)}',
    'logicalOrPattern(2)=${describeLogicalOrPattern(2)}',
    'logicalOrPattern(200)=${describeLogicalOrPattern(200)}',
    'logicalOrPattern(50)=${describeLogicalOrPattern(50)}',
    'labeledContinueToGuardedTarget(-5)=${describeLabeledContinueToGuardedTarget(-5)}',
    'labeledContinueToGuardedTarget(5)=${describeLabeledContinueToGuardedTarget(5)}',
  ];
}
