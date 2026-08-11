/// Function kinds (top-level, static, instance, local, anonymous),
/// block and arrow bodies, every parameter form with defaults, named
/// arguments interleaved with positional ones at a call site, and the
/// `void` and `Never` return types.
library;

/// A top-level function with a block body and two required positional
/// parameters.
int addTopLevel(int a, int b) {
  return a + b;
}

/// A top-level function with an arrow body.
int multiplyTopLevel(int a, int b) => a * b;

/// A top-level function exercising a required positional parameter
/// alongside an optional positional parameter with a default value.
String describeReading(String subject, int value, [String unit = 'units']) {
  return '$subject reads $value $unit';
}

/// A top-level function with two required positional parameters, one
/// required named parameter, and one defaulted named parameter.
String labelReading(
  String subject,
  num value, {
  required String category,
  bool approximate = false,
}) {
  final prefix = approximate ? '~' : '';
  return '$category: $subject=$prefix$value';
}

/// Calls [labelReading] with its named argument placed between the two
/// positional arguments, which Dart's call-site argument ordering
/// permits regardless of parameter declaration order.
String callLabelReadingWithInterleavedNamedArgument() {
  return labelReading('sensor', category: 'temperature', 41);
}

/// The log a [void]-returning function writes to.
final List<String> readingLog = <String>[];

/// A [void]-returning top-level function.
void logReading(String message) {
  readingLog.add(message);
}

/// A function whose return type is [Never]: it always throws and never
/// returns normally.
Never rejectReading(String reason) {
  throw StateError('rejected: $reason');
}

class ReadingStation {
  ReadingStation(this.name);

  final String name;

  static const int _baseOffset = 2;

  /// A static function: class-level, not tied to an instance.
  static int calibrationOffset(int raw) => raw + _baseOffset;

  /// An instance method with a block body that declares and calls a
  /// local function.
  int adjustedReading(int raw) {
    int square(int n) {
      return n * n;
    }

    return square(raw) + calibrationOffset(raw);
  }

  /// An instance method with an arrow body that passes an anonymous
  /// function (function literal) to a higher-order method.
  List<int> doubledReadings(List<int> raw) {
    return raw.map((value) => value * 2).toList();
  }
}
