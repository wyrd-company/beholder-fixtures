/// Conversions between `int` and `double`.
library;

List<String> describeConversions() {
  const wholeDouble = 4.0;
  const fractionalDouble = 4.7;
  const negativeFractional = -4.7;
  const source = 9;

  return <String>[
    'wholeDouble.toInt()=${wholeDouble.toInt()}',
    'fractionalDouble.truncate()=${fractionalDouble.truncate()}',
    'fractionalDouble.round()=${fractionalDouble.round()}',
    'fractionalDouble.floor()=${fractionalDouble.floor()}',
    'fractionalDouble.ceil()=${fractionalDouble.ceil()}',
    'negativeFractional.truncate()=${negativeFractional.truncate()}',
    'negativeFractional.floor()=${negativeFractional.floor()}',
    'source.toDouble()=${source.toDouble()}',
    'parsedInt=${int.parse('123')}',
    'parsedDouble=${double.parse('1.5')}',
    'triedParseInvalidInt=${int.tryParse('not-a-number')}',
  ];
}
