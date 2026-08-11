/// DART-CAN-FLOW-003: pattern taxonomy.
library;

/// A variable pattern (`final int n`), binding a new local.
String describeVariablePattern(Object? value) {
  if (value case final int n) {
    return 'int:$n';
  }
  return 'no-match';
}

/// An identifier pattern used as a wildcard (`_`), matching without binding.
String describeWildcardIdentifierPattern(Object? value) {
  return switch (value) {
    (_, final int y) => 'second:$y',
    _ => 'unmatched',
  };
}

const int kThreshold = 10;

/// A constant pattern: a literal and a reference to a declared `const`.
String describeConstantPattern(int value) {
  return switch (value) {
    0 => 'zero-literal',
    kThreshold => 'threshold-const',
    _ => 'other',
  };
}

/// A relational pattern (`< 0`, `== 0`, `> 100`), matching by comparison.
String describeRelationalPattern(int value) {
  return switch (value) {
    < 0 => 'negative',
    == 0 => 'zero',
    > 100 => 'large',
    _ => 'normal',
  };
}

/// A cast pattern (`x as int`): forces a runtime type cast within
/// destructuring, throwing only if the cast itself fails.
String describeCastPattern((num, Object) pair) {
  final (x as int, y as String) = pair;
  return 'x=$x y=$y';
}

/// A null-check pattern (`final v?`): matches only non-null values and binds
/// the unwrapped, non-nullable value.
String describeNullCheckPattern(String? value) {
  return switch (value) {
    final v? => 'present:$v',
    null => 'absent',
  };
}

/// A null-assert pattern (`v!`), nested inside a one-element record pattern:
/// matches unconditionally, asserting the value is non-null and throwing at
/// runtime if it is not.
int describeNullAssertPattern(int? value) {
  final (v!,) = (value,);
  return v * 2;
}

/// List patterns, including a rest element (`...rest`) that collects any
/// remaining elements.
String describeListPattern(List<int> values) {
  return switch (values) {
    [] => 'empty',
    [final only] => 'one:$only',
    [final first, ...final rest] => 'first=$first rest=$rest',
  };
}

/// A list pattern with an unnamed rest in the middle, matching a fixed head
/// and tail around any number of middle elements.
String describeListPatternWithMiddleRest(List<int> values) {
  if (values case [final first, ..., final last]) {
    return 'first=$first last=$last';
  }
  return 'too-short';
}

/// A map pattern, matching required keys and binding their values.
String describeMapPattern(Map<String, Object?> data) {
  return switch (data) {
    {'name': final String name, 'age': final int age} => '$name:$age',
    {'name': final String name} => name,
    _ => 'unknown',
  };
}

/// A positional record pattern.
String describeRecordPattern((int, int) point) => switch (point) {
  (0, 0) => 'origin',
  (final x, final y) => '$x,$y',
};

/// A named-field record pattern.
String describeNamedRecordPattern({required int x, required int y}) {
  final record = (x: x, y: y);
  return switch (record) {
    (x: 0, y: 0) => 'origin',
    (x: final rx, y: final ry) => '$rx,$ry',
  };
}

class PointObj {
  final int x;
  final int y;

  PointObj(this.x, this.y);
}

/// An object pattern, matching a type and destructuring its getters.
String describeObjectPattern(Object? value) {
  return switch (value) {
    PointObj(x: 0, y: 0) => 'origin',
    PointObj(x: final x, y: final y) => 'point:$x,$y',
    _ => 'not-a-point',
  };
}

/// A logical-and pattern: both sub-patterns must match the same value.
String describeLogicalAndPattern(Object? value) {
  return switch (value) {
    int n && > 0 => 'positive-int:$n',
    _ => 'other',
  };
}

/// A logical-or pattern: any sub-pattern matching is enough.
String describeTaxonomyLogicalOrPattern(Object? value) {
  return switch (value) {
    int() || double() => 'numeric',
    _ => 'non-numeric',
  };
}

/// A parenthesized pattern combined with a guard clause.
String describeParenthesizedPatternWithGuard(Object? value) {
  return switch (value) {
    (int n) when n > 10 => 'large:$n',
    (int n) => 'small:$n',
    _ => 'other',
  };
}

class Cluster {
  final List<(int, int)> points;

  Cluster(this.points);
}

/// A nested match: an object pattern whose field is destructured by a list
/// pattern, whose elements are destructured by record patterns.
String describeNestedMatch(Object? value) {
  return switch (value) {
    Cluster(points: [(final x0, final y0), ...final rest]) =>
      'first=($x0,$y0) restCount=${rest.length}',
    Cluster(points: []) => 'empty-cluster',
    _ => 'no-cluster',
  };
}

List<String> describePatternTaxonomy() {
  return <String>[
    'variablePattern=${describeVariablePattern(7)}',
    'variablePattern(no-match)=${describeVariablePattern('nope')}',
    'wildcardIdentifierPattern=${describeWildcardIdentifierPattern((1, 2))}',
    'constantPattern(0)=${describeConstantPattern(0)}',
    'constantPattern(10)=${describeConstantPattern(10)}',
    'constantPattern(4)=${describeConstantPattern(4)}',
    'relationalPattern(-5)=${describeRelationalPattern(-5)}',
    'relationalPattern(0)=${describeRelationalPattern(0)}',
    'relationalPattern(500)=${describeRelationalPattern(500)}',
    'relationalPattern(20)=${describeRelationalPattern(20)}',
    'castPattern=${describeCastPattern((1, 's'))}',
    'nullCheckPattern(present)=${describeNullCheckPattern('hi')}',
    'nullCheckPattern(absent)=${describeNullCheckPattern(null)}',
    'nullAssertPattern=${describeNullAssertPattern(21)}',
    'listPattern(empty)=${describeListPattern(const <int>[])}',
    'listPattern(one)=${describeListPattern(const <int>[5])}',
    'listPattern(many)=${describeListPattern(const <int>[1, 2, 3])}',
    'listPatternWithMiddleRest=${describeListPatternWithMiddleRest(const <int>[1, 2, 3, 4])}',
    'mapPattern(full)=${describeMapPattern(const <String, Object?>{'name': 'Ada', 'age': 30})}',
    'mapPattern(partial)=${describeMapPattern(const <String, Object?>{'name': 'Lin'})}',
    'recordPattern(origin)=${describeRecordPattern((0, 0))}',
    'recordPattern(point)=${describeRecordPattern((3, 4))}',
    'namedRecordPattern=${describeNamedRecordPattern(x: 1, y: 2)}',
    'objectPattern(origin)=${describeObjectPattern(PointObj(0, 0))}',
    'objectPattern(point)=${describeObjectPattern(PointObj(3, 4))}',
    'objectPattern(other)=${describeObjectPattern('nope')}',
    'logicalAndPattern=${describeLogicalAndPattern(5)}',
    'logicalOrPattern=${describeTaxonomyLogicalOrPattern(3.14)}',
    'parenthesizedPatternWithGuard(large)=${describeParenthesizedPatternWithGuard(50)}',
    'parenthesizedPatternWithGuard(small)=${describeParenthesizedPatternWithGuard(2)}',
    'nestedMatch=${describeNestedMatch(Cluster(const <(int, int)>[(1, 1), (2, 2), (3, 3)]))}',
    'nestedMatch(empty)=${describeNestedMatch(Cluster(const <(int, int)>[]))}',
  ];
}
