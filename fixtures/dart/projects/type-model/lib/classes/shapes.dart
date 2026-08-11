/// Classes, abstract declarations, and implicit interfaces, matching
/// [DART-CAN-TYPE-001]: `extends`, `implements`, inherited concrete members,
/// abstract members, overrides, and `super`; fields as getter/setter
/// contracts; implementing a concrete class as an interface without
/// inheriting its implementation.
library;

abstract class Shape {
  double get area;

  String describe() => 'shape with area ${area.toStringAsFixed(2)}';
}

class Circle extends Shape {
  Circle(this.radius);

  final double radius;

  @override
  double get area => 3.14159 * radius * radius;

  @override
  String describe() => 'Circle: ${super.describe()}';
}

class Square extends Shape {
  Square(this.side);

  final double side;

  @override
  double get area => side * side;
}

/// An abstract interface expressed purely as a getter/setter contract: any
/// implementer whose plain field induces the same accessor pair satisfies
/// it without declaring explicit `get`/`set` bodies.
abstract class Labeled {
  String get label;

  set label(String value);
}

class Tag implements Labeled {
  Tag(this.label);

  @override
  String label;
}

/// A concrete (non-abstract) class, used below as an implicit interface.
class Counter {
  Counter(this.value);

  int value;

  void increment() => value += 1;

  String describeCounter() => 'count=$value';
}

/// Implements [Counter] as an interface without inheriting its
/// implementation: every member is reimplemented independently, and
/// [increment] deliberately behaves differently from [Counter.increment].
class ManualCounter implements Counter {
  ManualCounter(this.value);

  @override
  int value;

  @override
  void increment() => value += 2;

  @override
  String describeCounter() => 'manual-count=$value';
}

String describeClasses() {
  final tag = Tag('initial');
  tag.label = 'updated';
  final manual = ManualCounter(0)..increment();

  return 'circle=${Circle(2).describe()} square=${Square(3).describe()} '
      'labeled=${tag.label} counter=${Counter(1).describeCounter()} '
      'manualCounter=${manual.describeCounter()}';
}
