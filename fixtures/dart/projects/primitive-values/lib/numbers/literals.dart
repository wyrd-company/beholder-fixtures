/// Decimal, hexadecimal, and digit-separated numeric literals, and numeric
/// literal context typing.
library;

const int decimalInt = 42;
const double decimalDouble = 3.14;
const int hexInt = 0xFF;
const int hexIntLowercase = 0x1a2b;
const int digitSeparatedInt = 1_000_000;
const int digitSeparatedHexInt = 0x1F_FF_00;
const double digitSeparatedDouble = 1_234.567_8;

/// An integer literal accepted directly where a `double` is expected; the
/// literal's static type follows the context type rather than `int`.
const double integerLiteralInDoubleContext = 5;

double _scaleByContextTypedLiteral(double factor) => factor * 2;

/// Calls [_scaleByContextTypedLiteral] with an integer literal argument,
/// exercising numeric literal context typing at a call site rather than a
/// variable declaration.
final double contextTypedArgumentResult = _scaleByContextTypedLiteral(10);

List<String> describeNumberLiterals() => <String>[
  'decimalInt=$decimalInt',
  'decimalDouble=$decimalDouble',
  'hexInt=$hexInt',
  'hexIntLowercase=$hexIntLowercase',
  'digitSeparatedInt=$digitSeparatedInt',
  'digitSeparatedHexInt=$digitSeparatedHexInt',
  'digitSeparatedDouble=$digitSeparatedDouble',
  'integerLiteralInDoubleContext=$integerLiteralInDoubleContext '
      '(runtimeType=${integerLiteralInDoubleContext.runtimeType})',
  'contextTypedArgumentResult=$contextTypedArgumentResult',
];
