/// UTF-16 code units versus Unicode scalar values (runes), and code-unit
/// versus scalar string length.
library;

/// A character outside the Basic Multilingual Plane, encoded in UTF-16 as a
/// surrogate pair.
const surrogatePairString = '\u{1F600}';

List<String> describeUnicode() {
  final codeUnits = surrogatePairString.codeUnits;
  final runes = surrogatePairString.runes.toList();
  final codeUnitLength = surrogatePairString.length;
  final scalarLength = surrogatePairString.runes.length;
  final contentEquality = surrogatePairString == '\u{1F600}';
  final firstScalar = surrogatePairString.runes.first;

  return <String>[
    'codeUnits=$codeUnits',
    'runes=$runes',
    'codeUnitLength=$codeUnitLength',
    'scalarLength=$scalarLength',
    'codeUnitLengthExceedsScalarLength=${codeUnitLength > scalarLength}',
    'contentEquality=$contentEquality',
    'firstScalar=U+${firstScalar.toRadixString(16).toUpperCase()}',
  ];
}
