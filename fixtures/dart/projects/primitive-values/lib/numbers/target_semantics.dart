/// Per-target numeric range, wrapping, identity, equality, and formatting
/// observations. Values are recorded as reported by the executing target;
/// they are not asserted to be portable across `vm-jit`/`native-aot`, `js`,
/// and `wasm`.
library;

List<String> describeNumberTargetObservations() {
  // Parsed rather than written as a literal: the exact 64-bit boundary
  // value is out of JavaScript's exactly representable integer range, so a
  // literal of this magnitude fails to compile there. Parsing observes the
  // per-target range difference instead of rejecting the js target.
  final nativeIntUpperBound = int.parse('9223372036854775807');
  final wrapped = nativeIntUpperBound + 1;
  final bitLength = nativeIntUpperBound.bitLength;
  final asDouble = nativeIntUpperBound.toDouble();
  final identicalLiterals = identical(1000000, 1000000);
  final equalAcrossTypes = 4 == 4.0;
  final identicalAcrossTypes = identical(4, 4.0);
  final formattedDouble = 1.0.toString();
  final formattedLargeDouble = 1e21.toString();

  // A whole-number `double` stored through `num`: whether it also answers
  // `is int` is target-dependent, since some targets represent whole-number
  // doubles and ints identically.
  final num wholeNumberAsNum = 4.0;
  final isIntCheck = wholeNumberAsNum is int;
  final isDoubleCheck = wholeNumberAsNum is double;

  return <String>[
    'nativeIntUpperBound=$nativeIntUpperBound',
    'wrapped=$wrapped',
    'bitLength=$bitLength',
    'asDouble=$asDouble',
    'identicalLiterals=$identicalLiterals',
    'equalAcrossTypes=$equalAcrossTypes',
    'identicalAcrossTypes=$identicalAcrossTypes',
    'formattedDouble=$formattedDouble',
    'formattedLargeDouble=$formattedLargeDouble',
    'isIntCheck=$isIntCheck',
    'isDoubleCheck=$isDoubleCheck',
  ];
}
