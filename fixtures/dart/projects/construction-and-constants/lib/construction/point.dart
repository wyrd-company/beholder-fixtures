/// Generative construction fixtures for [DART-CAN-OBJ-001]: an unnamed
/// constructor built from initializing formals and an initializer-list
/// assertion, alongside a named constructor built from a plain initializer
/// list, over final non-nullable fields.
library;

class Point {
  Point(this.x, this.y)
    : assert(x.isFinite, 'x must be finite'),
      assert(y.isFinite, 'y must be finite');

  /// Named constructor assigning both fields from a plain initializer list.
  Point.origin() : x = 0, y = 0;

  final double x;
  final double y;

  @override
  String toString() => 'Point($x, $y)';
}
