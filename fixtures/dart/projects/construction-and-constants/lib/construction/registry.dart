/// Synthesized and private construction fixtures for [DART-CAN-OBJ-002]: the
/// compiler-synthesized default constructor over an implicit `extends
/// Object`, a static-only utility with a private constructor, and a
/// private-constructor singleton.
library;

/// No constructor is declared, so the compiler synthesizes a public
/// zero-argument unnamed constructor. The class also has no `extends`
/// clause, so it implicitly extends [Object].
class Registry {}

/// A static-only class: every member is static, and the private constructor
/// prevents instantiation entirely.
class MeasurementUnits {
  MeasurementUnits._();

  static const double metersPerKilometer = 1000;
  static const double secondsPerHour = 3600;
}

/// A singleton built from a private constructor and a cached static
/// instance; the public surface exposes no way to construct another one.
class TokenVault {
  TokenVault._(this.id);

  static final TokenVault _instance = TokenVault._('root-vault');

  static TokenVault get instance => _instance;

  final String id;
}

/// Exercises the synthesized default constructor, the implicit `Object`
/// superclass, the static-only utility, and the singleton idiom.
List<String> describeRegistry() {
  final registry = Registry();
  // Widened to `dynamic` so the `is Object` check below reports a runtime
  // observation about the implicit superclass rather than a statically
  // known-true type test.
  final dynamic dynamicRegistry = registry;
  final firstAccess = TokenVault.instance;
  final secondAccess = TokenVault.instance;

  return <String>[
    'Registry() uses the synthesized default constructor: $registry',
    'Registry implicitly extends Object: ${dynamicRegistry is Object}',
    'MeasurementUnits is static-only: '
        '${MeasurementUnits.metersPerKilometer} m/km, '
        '${MeasurementUnits.secondsPerHour} s/h',
    'TokenVault.instance is a private-constructor singleton: '
        'id=${firstAccess.id}, sameInstance=${identical(firstAccess, secondAccess)}',
  ];
}
