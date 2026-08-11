/// Contextual and cross-unit inference, matching [DART-CAN-GEN-002]:
/// upward and downward inference for locals, top-levels, fields, literals,
/// closures, records, conditionals, switches, generic calls, and
/// overrides; inferred declarations across libraries; least-upper-bound
/// results. `inference_consumer.dart` is a second library depending on
/// this library's inferred top-level types.
library;

/// Downward inference: the empty list literal has no explicit type
/// argument, so it infers `<int>` from the declared `List<int>` context.
final List<int> downwardList = [];

/// Upward inference: the type is inferred purely from the initializer.
var upwardInferredTopLevel = 'inferred-as-string';

class InferenceHolder {
  /// Field inference: the type is inferred from the initializer.
  final inferredField = 42;
}

/// Downward inference into a list literal's elements from the declared
/// return type.
List<num> makeNumbers() => [1, 2.5, 3];

/// Closures: downward inference of a closure's parameter type from an
/// expected function-type context.
int Function(int) makeAdder(int amount) {
  return (value) => value + amount;
}

/// Downward inference into a record literal's field expressions.
(int, List<String>) makeRecordDownward() => (1, []);

/// Conditionals: the branches' least-upper-bound becomes the expression's
/// inferred type.
Object describeConditional(bool flag) => flag ? 1 : 'one';

/// A method whose parameter and return types are inferred from the
/// overridden member's signature (override inference).
class Base3 {
  num compute(num x) => x;
}

class Derived3 extends Base3 {
  @override
  compute(x) => x * 2;
}

String describeInference() {
  final holder = InferenceHolder();
  final numbers = makeNumbers();
  final adder = makeAdder(10);
  final recordDownward = makeRecordDownward();

  // Least-upper-bound across `switch` case results, inferred for a local
  // with no declared type.
  final switchLub = switch (2) {
    0 => 0,
    _ => 'non-zero',
  };

  // Generic-call inference: `T` inferred from the fill value's type.
  final inferredGenericCall = List.filled(3, 0);

  final derived = Derived3();

  return 'downwardList=$downwardList '
      'upwardInferredTopLevel=$upwardInferredTopLevel '
      'inferredField=${holder.inferredField} numbers=$numbers '
      'adder(5)=${adder(5)} recordDownward=$recordDownward '
      'conditionalTrue=${describeConditional(true)} '
      'conditionalFalse=${describeConditional(false)} '
      'switchLub=$switchLub inferredGenericCall=$inferredGenericCall '
      'overrideInferred=${derived.compute(4)}';
}
