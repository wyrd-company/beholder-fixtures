/// Operators, indexers, and callable objects, matching
/// [DART-CAN-TYPE-012]: representative unary and binary operators, `[]`,
/// `[]=`, `==`/`hashCode`, and `call`; a callable object assigned to a
/// function type; `>>>`.
library;

class Vector {
  const Vector(this.x, this.y);

  final int x;
  final int y;

  Vector operator +(Vector other) => Vector(x + other.x, y + other.y);

  Vector operator -() => Vector(-x, -y);

  Vector operator *(int scalar) => Vector(x * scalar, y * scalar);

  @override
  bool operator ==(Object other) =>
      other is Vector && other.x == x && other.y == y;

  @override
  int get hashCode => Object.hash(x, y);

  @override
  String toString() => '($x, $y)';
}

class Grid {
  Grid(int width, int height) : _cells = List<int>.filled(width * height, 0);

  final List<int> _cells;

  int operator [](int index) => _cells[index];

  void operator []=(int index, int value) => _cells[index] = value;
}

/// A callable object: instances can be invoked directly and assigned to a
/// matching function type.
class Adder {
  Adder(this.amount);

  final int amount;

  int call(int value) => value + amount;
}

class Bits {
  const Bits(this.value);

  final int value;

  Bits operator >>>(int shiftBy) => Bits(value >>> shiftBy);

  @override
  String toString() => value.toString();
}

String describeOperators() {
  const a = Vector(1, 2);
  const b = Vector(3, 4);

  final sum = a + b;
  final negated = -a;
  final scaled = a * 3;
  final equalToSelf = a == const Vector(1, 2);
  final hashesMatch = a.hashCode == const Vector(1, 2).hashCode;

  final grid = Grid(2, 2);
  grid[0] = 9;
  final indexed = grid[0];

  final addFive = Adder(5);
  final int Function(int) asFunction = addFive;
  final applied = asFunction(10);

  const bits = Bits(16);
  final shifted = bits >>> 2;
  final builtinUnsignedShift = -8 >>> 1;

  return 'sum=$sum negated=$negated scaled=$scaled equal=$equalToSelf '
      'hashesMatch=$hashesMatch indexed=$indexed callable=$applied '
      'shiftedBits=$shifted builtinShift=$builtinUnsignedShift';
}
