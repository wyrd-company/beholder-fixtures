/// Tear-offs of top-level, static, bound instance, generic, and
/// extension methods; a getter that returns a function value contrasted
/// with an ordinary method; and tear-off equality/identity across
/// those kinds.
library;

int square(int value) => value * value;

class MathToolkit {
  const MathToolkit(this.base);

  final int base;

  static int cube(int value) => value * value * value;

  /// A getter that returns a function value, contrasted with
  /// [addBaseMethod] below: reading this property evaluates the
  /// getter body and produces a closure, so calling it requires an
  /// extra pair of parentheses at the call site.
  int Function(int) get doubleBase =>
      (value) => value + base + base;

  /// An ordinary instance method reachable directly by call syntax or
  /// by tear-off.
  int addBaseMethod(int value) => value + base;

  /// A generic instance method whose type parameter is preserved by
  /// tear-off.
  T echo<T>(T value) => value;
}

extension NumberNaming on int {
  String named() => 'number($this)';
}

/// Tears off the top-level [square] function.
int Function(int) tearOffTopLevel() => square;

/// Tears off the static [MathToolkit.cube] method.
int Function(int) tearOffStatic() => MathToolkit.cube;

/// Tears off an instance method bound to [toolkit].
int Function(int) tearOffBound(MathToolkit toolkit) => toolkit.addBaseMethod;

/// Tears off a generic instance method, preserving its type parameter.
T Function<T>(T) tearOffGeneric(MathToolkit toolkit) => toolkit.echo;

/// Tears off an extension method.
String Function() tearOffExtension(int value) => value.named;

/// Contrasts reading [MathToolkit.doubleBase] (a getter that returns a
/// function value, so the property read alone does not run
/// [MathToolkit.base]'s doubling) with tearing off and calling the
/// ordinary [MathToolkit.addBaseMethod] method.
class GetterVersusMethod {
  const GetterVersusMethod({
    required this.getterFunction,
    required this.getterInvoked,
    required this.methodTearOff,
    required this.methodInvoked,
  });

  final int Function(int) getterFunction;
  final int getterInvoked;
  final int Function(int) methodTearOff;
  final int methodInvoked;
}

GetterVersusMethod compareGetterAndMethod(MathToolkit toolkit) {
  final getterFunction = toolkit.doubleBase;
  final methodTearOff = toolkit.addBaseMethod;
  return GetterVersusMethod(
    getterFunction: getterFunction,
    getterInvoked: getterFunction(3),
    methodTearOff: methodTearOff,
    methodInvoked: methodTearOff(3),
  );
}

/// Compares identity and equality across tear-off kinds: two tear-offs
/// of the same top-level or static function are canonicalized and
/// therefore identical to each other, while two tear-offs of the same
/// bound instance method on the same receiver compare equal without
/// being guaranteed identical.
class TearOffComparison {
  const TearOffComparison({
    required this.topLevelIdentical,
    required this.staticIdentical,
    required this.boundEqual,
  });

  final bool topLevelIdentical;
  final bool staticIdentical;
  final bool boundEqual;
}

TearOffComparison compareTearOffs(MathToolkit toolkit) {
  return TearOffComparison(
    topLevelIdentical: identical(tearOffTopLevel(), tearOffTopLevel()),
    staticIdentical: identical(tearOffStatic(), tearOffStatic()),
    boundEqual: tearOffBound(toolkit) == tearOffBound(toolkit),
  );
}
