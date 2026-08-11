/// Arithmetic operators, truncating division, modulo, shifts, and an
/// overflow-sensitive left shift.
library;

List<String> describeArithmetic() {
  const a = 17;
  const b = 5;
  final sum = a + b;
  final difference = a - b;
  final product = a * b;
  final quotient = a / b;
  final truncatingQuotient = a ~/ b;
  final remainder = a % b;
  final negativeRemainder = -a % b;
  final leftShift = 1 << 4;
  final rightShift = -8 >> 1;
  final unsignedRightShift = -8 >>> 1;

  // Overflow-sensitive: shifting a 64-bit int left past its sign bit wraps
  // into a negative value rather than growing arbitrarily.
  final overflowingLeftShift = 1 << 63;

  return <String>[
    'sum=$sum',
    'difference=$difference',
    'product=$product',
    'quotient=$quotient',
    'truncatingQuotient=$truncatingQuotient',
    'remainder=$remainder',
    'negativeRemainder=$negativeRemainder',
    'leftShift=$leftShift',
    'rightShift=$rightShift',
    'unsignedRightShift=$unsignedRightShift',
    'overflowingLeftShift=$overflowingLeftShift',
  ];
}
