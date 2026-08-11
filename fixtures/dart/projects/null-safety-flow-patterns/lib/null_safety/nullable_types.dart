/// DART-CAN-NULL-001: nullable and non-nullable types.
library;

/// A non-nullable type parameter bound to a nullable bound (`T extends
/// num?`), so `T` may itself be instantiated with a nullable type argument.
class Reading<T extends num?> {
  final T value;

  const Reading(this.value);

  bool get isPresent => value != null;
}

/// A plain generic holder used with both non-nullable (`T`) and nullable
/// (`T?`) type arguments at its call sites below.
class Slot<T> {
  final T value;

  const Slot(this.value);
}

/// A field typed `T` (non-nullable) alongside a field typed `T?` (nullable),
/// and a nullable-typed parameter and return.
class Sensor {
  final String id; // non-nullable field: T
  double? lastReading; // nullable field: T?

  Sensor(this.id, this.lastReading);

  /// A nullable parameter and a nullable return type.
  String describe(String? unit) {
    final reading = lastReading;
    if (unit == null) {
      return reading == null ? 'unset' : '$reading';
    }
    return reading == null ? 'unset $unit' : '$reading $unit';
  }

  /// A nullable return type with no nullable parameter.
  double? readOrNull() => lastReading;
}

/// The `Null` type used explicitly, both as a return type and as a value.
Null noop() => null;

/// A base declaring a nullable parameter and a nullable return.
abstract class Renderer {
  String? render(int? input);
}

/// Overriding with a *wider* (contravariant) parameter type (`num?` accepts
/// every `int?`) is nullability-override-compatible.
class WideningRenderer extends Renderer {
  @override
  String? render(num? input) => input == null ? null : 'num:$input';
}

/// Overriding with a *narrower* (covariant) non-nullable return type
/// (`String` is a subtype of the declared `String?`) is also
/// nullability-override-compatible.
class NonNullReturningRenderer extends Renderer {
  @override
  String render(int? input) => input == null ? 'null' : 'int:$input';
}

/// Nullable type arguments on collection and holder types: `List<int?>`,
/// `Slot<int?>`, and a non-nullable counterpart `Slot<int>` for contrast.
final List<int?> nullableInts = <int?>[1, null, 3];
final Slot<int?> nullableSlot = Slot<int?>(null);
final Slot<int> nonNullSlot = Slot<int>(7);

/// `Reading<double?>` instantiates the nullable-bounded parameter with a
/// nullable type argument; `Reading<double>` instantiates it with a
/// non-nullable one.
final Reading<double?> nullableReading = Reading<double?>(null);
final Reading<double> nonNullReading = Reading<double>(98.6);

/// `Never?`: `Never` has no instances, so a `Never?`-typed value can only
/// ever be `null` at runtime. Dart's type normalization rewrites `Never?`
/// to `Null`, so the two are the same type — only the source spelling
/// differs. The `Never?` parameter and return type are exercised here.
Never? identityOfNever(Never? input) => input;

List<String> describeNullableTypes() {
  final sensor = Sensor('sensor-a', null);
  final widening = WideningRenderer();
  final nonNullReturning = NonNullReturningRenderer();
  return <String>[
    'noop()=${noop()}',
    'sensor.describe(null)=${sensor.describe(null)}',
    'sensor.describe("C")=${sensor.describe('C')}',
    'sensor.readOrNull()=${sensor.readOrNull()}',
    'nullableInts=$nullableInts',
    'nullableSlot.value=${nullableSlot.value}',
    'nonNullSlot.value=${nonNullSlot.value}',
    'nullableReading.isPresent=${nullableReading.isPresent}',
    'nonNullReading.isPresent=${nonNullReading.isPresent}',
    'identityOfNever(null)=${identityOfNever(null)}',
    'widening.render(3)=${widening.render(3)}',
    'widening.render(null)=${widening.render(null)}',
    'nonNullReturning.render(4)=${nonNullReturning.render(4)}',
  ];
}
