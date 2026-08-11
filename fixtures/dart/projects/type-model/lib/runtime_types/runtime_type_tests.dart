/// Type tests, casts, literals, and runtime type, matching
/// [DART-CAN-TYPE-010]: `is`, `is!`, `as`, generic type tests, type
/// literals, and `runtimeType`; reified generic arguments; type objects as
/// values.
library;

class Box<T> {
  const Box(this.value);

  final T value;
}

String describeRuntimeTypes() {
  final Object value = Box<int>(5);

  final isBox = value is Box<int>;
  final isNotString = value is! String;
  final asBox = value as Box<int>;

  // Generic type test against a reified type argument. `numbers` is widened
  // to `Object` first so the test is a genuine runtime check rather than a
  // statically-known-true comparison.
  final Object numbers = <int>[1, 2, 3];
  final isIntList = numbers is List<int>;
  final isStringList = numbers is List<String>;

  // Type literals as first-class values.
  const Type intType = int;
  final Type boxType = value.runtimeType;

  // Reified generic arguments: `runtimeType` reflects the actual type
  // argument used at construction, not merely the static type.
  final Box<String> stringBox = Box<String>('s');

  return 'isBox=$isBox isNotString=$isNotString asBoxValue=${asBox.value} '
      'isIntList=$isIntList isStringList=$isStringList intType=$intType '
      'boxType=$boxType stringBoxRuntimeType=${stringBox.runtimeType} '
      'typeObjectEquality=${boxType == Box<int>}';
}
