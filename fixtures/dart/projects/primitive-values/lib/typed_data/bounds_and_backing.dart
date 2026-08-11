/// Typed-data bounds behavior and a native-versus-JavaScript backing
/// observation for typed-list representation. Backing representation is
/// recorded, not asserted portable across targets.
library;

import 'dart:typed_data';

List<String> describeBoundsAndBacking() {
  final list = Uint8List(4);

  String outOfRangeIndexResult;
  try {
    // ignore: unused_local_variable
    final value = list[10];
    outOfRangeIndexResult = 'no error (unexpected): $value';
  } on RangeError catch (error) {
    outOfRangeIndexResult = 'RangeError: ${error.message}';
  }

  String outOfRangeViewResult;
  try {
    // A 10-element Int32List view needs 40 bytes; the source buffer only
    // has 4.
    list.buffer.asInt32List(0, 10);
    outOfRangeViewResult = 'no error (unexpected)';
  } on RangeError catch (error) {
    outOfRangeViewResult = 'RangeError: ${error.message}';
  } on ArgumentError catch (error) {
    outOfRangeViewResult = 'ArgumentError: ${error.message}';
  }

  // A value outside the 8-bit unsigned range wraps modulo 256 when stored.
  final wrappingList = Uint8List(1)..[0] = 300;

  return <String>[
    'outOfRangeIndexResult=$outOfRangeIndexResult',
    'outOfRangeViewResult=$outOfRangeViewResult',
    'wrappedByteValue=${wrappingList[0]}',
    'elementSizeInBytes=${list.elementSizeInBytes}',
  ];
}

/// Values whose in-memory representation is target-defined: a native byte
/// buffer on `vm-jit`/`native-aot` versus a JavaScript-backed typed array
/// on `js`/`wasm`.
List<String> describeTypedDataBackingObservations() {
  // Parsed rather than written as literals: this magnitude is out of
  // JavaScript's exactly representable integer range, so literals of this
  // size fail to compile there.
  final ints = Int64List.fromList(<int>[
    int.parse('9223372036854775807'),
    int.parse('-9223372036854775808'),
  ]);
  final floats = Float64List.fromList(<double>[0.1 + 0.2]);
  final firstByteOfInt64Buffer = Uint8List.view(ints.buffer)[0];

  return <String>[
    'int64Values=${ints.toList()}',
    'float64SumRepresentation=${floats[0]}',
    'firstByteOfInt64Buffer=$firstByteOfInt64Buffer',
    'int64BufferLengthInBytes=${ints.buffer.lengthInBytes}',
  ];
}
