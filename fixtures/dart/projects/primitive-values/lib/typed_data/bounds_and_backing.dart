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
/// buffer on `vm-jit`/`native-aot`/`wasm` versus a JavaScript-backed typed
/// array on `js`, where `Int64List`/`Uint64List` are unsupported at
/// runtime. The unsupported case is itself the `js` backing observation,
/// recorded rather than left to throw past the rest of this function.
List<String> describeTypedDataBackingObservations() {
  final observations = <String>[];

  try {
    // Parsed rather than written as literals: this magnitude is out of
    // JavaScript's exactly representable integer range, so literals of
    // this size fail to compile there.
    final ints = Int64List.fromList(<int>[
      int.parse('9223372036854775807'),
      int.parse('-9223372036854775808'),
    ]);
    observations.add('int64Values=${ints.toList()}');
    observations.add('int64BufferLengthInBytes=${ints.buffer.lengthInBytes}');
  } on UnsupportedError catch (error) {
    observations.add('int64Backing=unsupported: ${error.message}');
  }

  // Float64List is backed on every declared target, so this observation
  // always completes.
  final floats = Float64List.fromList(<double>[0.1 + 0.2]);
  final firstByteOfFloatBuffer = Uint8List.view(floats.buffer)[0];

  observations.add('float64SumRepresentation=${floats[0]}');
  observations.add('firstByteOfFloatBuffer=$firstByteOfFloatBuffer');

  return observations;
}
