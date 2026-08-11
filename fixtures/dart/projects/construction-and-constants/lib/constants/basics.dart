/// Constant-expression subset fixtures for [DART-CAN-CONST-001]: const
/// variables, primitive operations, strings, symbols, type/function/
/// constructor literals, collections, records, annotations, const
/// constructors with potentially-constant initializers, an implicit const
/// context, a generic constant, and an environment constant.
library;

/// A const-constructible value type whose initializer is only
/// potentially-constant: the assertion depends on the constructor's own
/// parameter rather than on a value known independent of any call site.
class Money {
  const Money(this.cents) : assert(cents >= 0, 'cents must not be negative');

  final int cents;

  @override
  String toString() => '\$${cents / 100}';
}

/// A generic const-constructible wrapper, used below to exercise a generic
/// constant.
class Wrapper<T> {
  const Wrapper(this.value);

  final T value;
}

/// A const annotation class.
class FixtureTag {
  const FixtureTag(this.name);

  final String name;
}

@FixtureTag('constant-subset-demo')
class AnnotatedSubject {
  const AnnotatedSubject();
}

// Const variables of primitive types.
const int answer = 42;
const double ratio = 0.5;
const bool enabled = true;

// Primitive operations over const operands.
const int sum = answer + 8;
const bool flag = enabled && (answer > 0);

// Const strings, including const string interpolation.
const String greeting = 'hello';
const String templated = 'answer=$answer';

// A const symbol literal.
const Symbol answerSymbol = #answer;

// A const type literal.
const Type intType = int;

// A top-level static function torn off as a constant function value.
const int Function(String) parseIntConst = int.parse;

// A const constructor invocation (constructor literal).
const Money price = Money(500);

// Const collections. The list literal establishes an implicit const
// context, so the nested `Money(100)`/`Money(200)` need no explicit `const`.
const List<Money> prices = <Money>[Money(100), Money(200)];
const Map<String, int> counts = <String, int>{'a': 1, 'b': 2};
const Set<int> uniqueNumbers = <int>{1, 2, 3};

// Const records: a positional record and a named-field record.
const (int, String) pair = (1, 'one');
const ({int x, int y}) namedPair = (x: 1, y: 2);

// A generic constant.
const Wrapper<int> wrappedInt = Wrapper<int>(7);

// Environment constants, each falling back to its default when the
// corresponding `-D` define is not supplied.
const String buildFlavor = String.fromEnvironment(
  'FIXTURE_FLAVOR',
  defaultValue: 'default',
);
const int retries = int.fromEnvironment('FIXTURE_RETRIES', defaultValue: 3);
const bool productMode = bool.fromEnvironment('dart.vm.product');

List<String> describeConstantSubset() {
  return <String>[
    'Primitive const operations: sum=$sum, flag=$flag',
    'Const string interpolation: $templated, greeting=$greeting',
    'Const symbol: $answerSymbol',
    'Const type literal: $intType',
    'Const function literal invoked: ${parseIntConst('99')}',
    'Const constructor invocation: $price',
    'Const collections (implicit const context for nested Money): $prices, '
        '$counts, $uniqueNumbers',
    'Const records: $pair, $namedPair',
    'Generic constant: ${wrappedInt.value}',
    'Environment constants: buildFlavor=$buildFlavor, retries=$retries, '
        'productMode=$productMode',
    'Const annotation present on AnnotatedSubject (see @FixtureTag above).',
  ];
}
