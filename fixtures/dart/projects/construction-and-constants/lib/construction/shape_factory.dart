/// Factory and redirection fixtures for [DART-CAN-OBJ-003]: a caching,
/// subtype-returning factory; a cross-type redirecting factory; a same-class
/// redirecting generative constructor; generic factory forwarding; a
/// redirect chain; and a const factory redirect.
library;

/// Base of a small shape hierarchy. Its factory constructors return
/// subtypes rather than allocating `Shape` directly.
abstract class Shape {
  Shape(this.sides);

  final int sides;

  double get area;

  static final Map<int, Shape> _sidesCache = <int, Shape>{};

  /// Caching, subtype-returning factory: repeated calls with the same
  /// [sides] return the identical cached instance.
  factory Shape.withSides(int sides) {
    return _sidesCache.putIfAbsent(
      sides,
      () => sides == 3 ? Triangle(1, 1) : Square(1),
    );
  }

  /// Cross-type redirecting factory: forwards to [Square.unit] in a
  /// different class.
  factory Shape.unit() = Square.unit;
}

class Square extends Shape {
  Square(this.side) : super(4);

  /// Same-class redirecting generative constructor.
  Square.unit() : this(1);

  final double side;

  @override
  double get area => side * side;
}

class Triangle extends Shape {
  Triangle(this.base, this.height) : super(3);

  final double base;
  final double height;

  @override
  double get area => 0.5 * base * height;
}

/// Generic redirecting factory forwarding to a private implementation type.
abstract class Box<T> {
  factory Box(T value) = _BoxImpl<T>;

  T get value;
}

class _BoxImpl<T> implements Box<T> {
  _BoxImpl(this.value);

  @override
  final T value;
}

/// A redirect chain: [Container.wrapping] is a factory that redirects to
/// [Container.of], which is a generative constructor that redirects to the
/// unnamed generative constructor.
class Container<T> {
  Container(this.value);

  Container.of(T value) : this(value);

  factory Container.wrapping(T value) = Container.of;

  final T value;
}

/// A small const-constructible value type with a const factory redirect.
class Coord {
  const Coord(this.x, this.y);

  /// Const factory redirect to a private const generative constructor.
  const factory Coord.zero() = Coord._origin;

  const Coord._origin() : x = 0, y = 0;

  final double x;
  final double y;

  @override
  String toString() => 'Coord($x, $y)';
}

List<String> describeShapeFactories() {
  final firstSquare = Shape.withSides(4);
  final secondSquare = Shape.withSides(4);
  final unitSquare = Shape.unit();
  final chainedContainer = Container<int>.wrapping(9);
  final box = Box<String>('boxed');
  const coordZero = Coord.zero();
  const coordOrigin = Coord(0, 0);

  return <String>[
    'Shape.withSides(4) caches by sides: sameInstance='
        '${identical(firstSquare, secondSquare)}, area=${firstSquare.area}',
    'Shape.unit() cross-type redirects to Square.unit(): '
        'runtimeType=${unitSquare.runtimeType}, side=${(unitSquare as Square).side}',
    'Container.wrapping(9) redirect chain resolves to value: '
        '${chainedContainer.value}',
    'Box<String>("boxed") generic forwarding resolves to value: ${box.value}',
    'const Coord.zero() const factory redirect canonicalizes: '
        'sameInstance=${identical(coordZero, coordOrigin)}',
  ];
}
