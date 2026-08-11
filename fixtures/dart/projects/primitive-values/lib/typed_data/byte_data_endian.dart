/// `ByteData` reads and writes with explicit little-endian and big-endian
/// byte order.
library;

import 'dart:typed_data';

List<String> describeByteDataEndian() {
  final data = ByteData(8);
  data.setInt32(0, 0x01020304, Endian.little);
  data.setInt32(4, 0x01020304, Endian.big);

  final littleEndianBytes = <int>[for (var i = 0; i < 4; i++) data.getUint8(i)];
  final bigEndianBytes = <int>[for (var i = 4; i < 8; i++) data.getUint8(i)];

  final roundTrippedLittle = data.getInt32(0, Endian.little);
  final roundTrippedBig = data.getInt32(4, Endian.big);
  final misreadAsOppositeEndian = data.getInt32(0, Endian.big);

  return <String>[
    'littleEndianBytes=$littleEndianBytes',
    'bigEndianBytes=$bigEndianBytes',
    'roundTrippedLittle=$roundTrippedLittle',
    'roundTrippedBig=$roundTrippedBig',
    'misreadAsOppositeEndian=$misreadAsOppositeEndian',
  ];
}
