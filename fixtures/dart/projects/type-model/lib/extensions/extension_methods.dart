/// Extension methods, matching [DART-CAN-TYPE-005]: named, unnamed,
/// private, generic, bounded, nullable-target, getter, operator, static,
/// and explicit extension forms; prefixed explicit application; extension
/// tear-off; instance-member precedence; most-specific extension
/// selection; a `dynamic` bypass; a nullable receiver including `null`.
library;

import 'extension_boundary.dart' as boundary;

/// A named extension.
extension NumberOps on int {
  int doubled() => this * 2;
}

/// An unnamed extension.
extension on String {
  String shout() => '${toUpperCase()}!';
}

/// A private extension, visible only within this library.
extension _PrivateOps on int {
  int tripled() => this * 3;
}

/// A generic, bounded extension with a getter.
extension BoundedOps<T extends num> on List<T> {
  T get largest => reduce((a, b) => a > b ? a : b);
}

/// A nullable-target extension: applicable even when the receiver's actual
/// value is `null`.
extension NullableGreeting on String? {
  String greet() => this == null ? 'hello, stranger' : 'hello, $this';
}

class Vector2 {
  const Vector2(this.x, this.y);

  final int x;
  final int y;

  @override
  String toString() => '($x, $y)';
}

/// An extension supplying operators, a getter, and a static member.
extension Vector2Ops on Vector2 {
  Vector2 operator +(Vector2 other) => Vector2(x + other.x, y + other.y);

  Vector2 operator -() => Vector2(-x, -y);

  int get magnitudeSquared => x * x + y * y;

  static Vector2 zero() => const Vector2(0, 0);
}

class Greeter {
  String greet() => 'instance greet';
}

/// Shadowed by [Greeter.greet]: an implicit call always resolves to the
/// instance member (instance-member precedence). The explicit extension
/// application form, `GreeterExt(value).greet()`, reaches this method
/// anyway.
extension GreeterExt on Greeter {
  String greet() => 'extension greet';
}

extension ObjectDescribe on Object {
  String describeSpecificity() => 'Object extension';
}

/// Applicable to the same receivers as [ObjectDescribe], but more specific:
/// an `int` receiver resolves here rather than to [ObjectDescribe], with no
/// ambiguity error.
extension IntDescribe on int {
  String describeSpecificity() => 'int extension';
}

String describeExtensions() {
  final greeter = Greeter();
  String? maybeNull;

  // Extension tear-off: torn off like any other method, resolved statically
  // at the tear-off site.
  final int Function() doubler = 5.doubled;

  // `dynamic` bypass: extension methods are resolved statically against the
  // receiver's static type, so a `dynamic`-typed receiver bypasses
  // extension lookup entirely — the call is instead dispatched as an
  // ordinary dynamic member access against `int`, which has no `doubled`
  // member, so it throws.
  dynamic dynValue = 5;
  var dynamicBypassObserved = false;
  try {
    dynValue.doubled();
  } on NoSuchMethodError {
    dynamicBypassObserved = true;
  }

  // Explicit extension application forces static resolution despite the
  // dynamic receiver, avoiding the bypass.
  final viaExplicitApplication = NumberOps(dynValue as int).doubled();

  return 'doubled=${5.doubled()} shout=${'hi'.shout()} '
      'tripled=${5.tripled()} largest=${<int>[3, 9, 4].largest} '
      'nullGreeting=${maybeNull.greet()} valueGreeting=${'traveler'.greet()} '
      'vectorSum=${Vector2Ops(const Vector2(1, 2)) + const Vector2(3, 4)} '
      'vectorNeg=${-const Vector2(1, 2)} '
      'vectorMagSq=${const Vector2(3, 4).magnitudeSquared} '
      'vectorZero=${Vector2Ops.zero()} '
      'implicitGreet=${greeter.greet()} '
      'explicitGreet=${GreeterExt(greeter).greet()} '
      'mostSpecific=${5.describeSpecificity()} '
      'tornOffDoubler=${doubler()} '
      'dynamicBypassObserved=$dynamicBypassObserved '
      'dynamicBypassAvoidedByExplicitApplication=$viaExplicitApplication '
      'prefixedExplicit=${boundary.BoundaryOps(3).quadrupled()}';
}
