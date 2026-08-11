/// Extension types, matching [DART-CAN-TYPE-006]: representation,
/// constructors, members, operators, static members, generics, and
/// `implements`; static distinction and runtime erasure; `@redeclare`;
/// nullable representation; casts; contrast with class wrappers or
/// extension methods. The JavaScript-interop variant of this item is owned
/// by `platforms-and-interop`; this library covers static distinction and
/// runtime erasure only.
///
/// This project otherwise uses SDK libraries only; it vendors a pinned
/// `package:meta` (see `pubspec.yaml`) solely for the `@redeclare`
/// annotation below.
library;

import 'package:meta/meta.dart';

/// A primitive-representation extension type with a named constructor,
/// members, an operator, and a static member.
extension type Meters(double value) {
  Meters.fromCentimeters(double cm) : value = cm / 100;

  Meters operator +(Meters other) => Meters(value + other.value);

  double get inFeet => value * 3.28084;

  static Meters zero() => Meters(0);

  String format() => '${value}m';
}

/// A nullable-representation extension type.
extension type MaybeMeters(double? value) {
  bool get hasValue => value != null;
}

/// A generic extension type.
extension type Cell<T>(T value) {
  T unwrap() => value;
}

class RawLog {
  final List<String> entries = <String>[];

  void add(String entry) => entries.add(entry);

  String get summary => entries.join(', ');
}

/// `implements` a class interface whose representation type (`RawLog`) is
/// itself the implemented type, so unredeclared members ([summary],
/// [entries]) forward transparently to the representation object. [add]
/// deliberately replaces the forwarded member instead, marked `@redeclare`
/// to record that replacement as intentional rather than an accidental
/// signature mismatch.
extension type Log(RawLog raw) implements RawLog {
  @redeclare
  void add(String entry) => raw.add('[logged] $entry');
}

/// Contrast: a genuine class wrapper allocates its own heap object with a
/// runtime type distinct from [double], unlike [Meters], which erases to
/// its representation type at runtime with no wrapper allocation at all.
/// An extension method (see `extensions/extension_methods.dart`) goes
/// further still: it adds behavior without introducing any new static type
/// whatsoever.
class MetersWrapper {
  const MetersWrapper(this.value);

  final double value;
}

void takesMeters(Meters m) {}

String describeExtensionTypes() {
  final meters = Meters(100);
  final fromCm = Meters.fromCentimeters(250);
  final sum = meters + fromCm;

  // Static distinction: a bare `double` cannot be passed where `Meters` is
  // expected without wrapping, even though they share a runtime
  // representation.
  takesMeters(Meters(5));

  // Casts and runtime erasure: at runtime, `meters` IS a `double`, so a
  // cast to the representation type succeeds, and an `is` test against the
  // extension type name succeeds against the same erased representation.
  final raw = meters as double;
  final isMeters = raw is Meters;

  final maybe = MaybeMeters(null);
  final present = MaybeMeters(2.5);

  final cell = Cell<String>('boxed');

  final log = Log(RawLog())
    ..add('first')
    ..add('second');

  return 'meters=${meters.format()} fromCm=${fromCm.format()} '
      'sum=${sum.format()} raw=$raw isMeters=$isMeters '
      'inFeet=${meters.inFeet.toStringAsFixed(2)} '
      'zero=${Meters.zero().format()} maybeHasValue=${maybe.hasValue} '
      'presentHasValue=${present.hasValue} cell=${cell.unwrap()} '
      'logSummary=${log.summary} '
      'wrapperRuntimeType=${const MetersWrapper(1).runtimeType}';
}
