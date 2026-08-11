/// Byte buffers, typed lists, overlapping views over one buffer, and the
/// typed-list view kinds this project exercises.
library;

import 'dart:typed_data';

List<String> describeBuffersAndViews() {
  final bytes = Uint8List.fromList(<int>[
    0x01,
    0x02,
    0x03,
    0x04,
    0x05,
    0x06,
    0x07,
    0x08,
  ]);
  final buffer = bytes.buffer;

  // Overlapping views: an Int32List and a Uint16List both backed by the
  // same underlying buffer as the source Uint8List.
  final asInt32 = buffer.asInt32List();
  final asUint16 = buffer.asUint16List();

  // A write through one view is visible through another view over the same
  // buffer.
  bytes[0] = 0xff;
  final observedThroughInt32AfterMutation = asInt32[0];

  final supportedViewKinds = <String, TypedData>{
    'Int8List': Int8List.fromList(<int>[-1]),
    'Uint8List': Uint8List.fromList(<int>[1]),
    'Uint8ClampedList': Uint8ClampedList.fromList(<int>[300]),
    'Int16List': Int16List.fromList(<int>[-1]),
    'Uint16List': Uint16List.fromList(<int>[1]),
    'Int32List': Int32List.fromList(<int>[-1]),
    'Uint32List': Uint32List.fromList(<int>[1]),
    'Int64List': Int64List.fromList(<int>[-1]),
    'Uint64List': Uint64List.fromList(<int>[1]),
    'Float32List': Float32List.fromList(<double>[1.5]),
    'Float64List': Float64List.fromList(<double>[1.5]),
  };

  return <String>[
    'bufferLengthInBytes=${buffer.lengthInBytes}',
    'asInt32Length=${asInt32.length}',
    'asUint16Length=${asUint16.length}',
    'observedThroughInt32AfterMutation=$observedThroughInt32AfterMutation',
    for (final entry in supportedViewKinds.entries)
      '${entry.key}(lengthInBytes=${entry.value.lengthInBytes})',
  ];
}
