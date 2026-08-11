/// Class modifiers and capability restrictions, matching
/// [DART-CAN-TYPE-002]: `base`, `interface`, `final`, `sealed`, abstract
/// combinations, `mixin class`, and `base mixin`. This library declares
/// every modified type; `modifiers_boundary.dart` is a second library that
/// extends, implements, and mixes several of them in from outside this
/// declaring library.
library;

base class Animal {
  Animal(this.name);

  final String name;

  String speak() => '$name makes a sound';
}

interface class Sound {
  String describe() => 'a sound';
}

final class Lock {
  Lock(this.combination);

  final int combination;

  String describeLock() => 'lock($combination)';
}

/// A sealed class: every direct subtype lives in this same library, which
/// lets [describeShape2]'s `switch` be exhaustive with no default case.
sealed class Shape2 {
  double get area;
}

class Circle2 extends Shape2 {
  Circle2(this.radius);

  final double radius;

  @override
  double get area => 3.14159 * radius * radius;
}

class Square2 extends Shape2 {
  Square2(this.side);

  final double side;

  @override
  double get area => side * side;
}

String describeShape2(Shape2 shape) => switch (shape) {
  Circle2(radius: final r) => 'circle(r=$r) area=${shape.area}',
  Square2(side: final s) => 'square(s=$s) area=${shape.area}',
};

/// A `mixin class`: usable both as an ordinary superclass (`extends`) and
/// as a mixin (`with`).
mixin class Flyer {
  String flightReport() => 'flying';
}

/// A `base mixin`: mixing it in from another library requires the mixing
/// class to also be `base`, `final`, or `sealed`, exercised by
/// `modifiers_boundary.dart`.
base mixin Swimmer on Animal {
  String swimReport() => '$name swims';
}

abstract base class AbstractVehicle {
  AbstractVehicle(this.model);

  final String model;

  String startEngine();

  String describeVehicle() => '$model: ${startEngine()}';
}

abstract interface class Describable {
  String describe();
}

/// An `abstract final class` used purely as a static-member namespace: it
/// can be neither instantiated, extended, nor implemented anywhere.
abstract final class MathHelpers {
  static int doubleValue(int x) => x * 2;
}
