/// DART-CAN-COLL-001: collection literal kinds and inference.
library;

/// A mutable list literal with an explicit type argument.
final List<int> explicitTypedList = <int>[1, 2, 3];

/// A mutable list literal whose element type is inferred from the
/// contextual (declared) type instead of being written explicitly.
List<int> buildContextuallyTypedList() {
  final List<int> list = [1, 2, 3];
  return list;
}

/// A const list literal.
const List<int> constList = <int>[1, 2, 3];

/// A mutable set literal with an explicit type argument.
final Set<String> explicitTypedSet = <String>{'a', 'b'};

/// A mutable set literal whose element type is inferred contextually.
Set<String> buildContextuallyTypedSet() {
  final Set<String> set = {'a', 'b'};
  return set;
}

/// A const set literal.
const Set<String> constSet = <String>{'x', 'y'};

/// A mutable map literal with explicit type arguments.
final Map<String, int> explicitTypedMap = <String, int>{'a': 1};

/// A mutable map literal whose key/value types are inferred contextually.
Map<String, int> buildContextuallyTypedMap() {
  final Map<String, int> map = {'a': 1};
  return map;
}

/// A const map literal.
const Map<String, int> constMap = <String, int>{'k': 1};

/// `{}` with no type context and no elements defaults to a map, not a set.
final Map<dynamic, dynamic> defaultBraceLiteral = {};

/// An empty list literal, whose element type is inferred entirely from its
/// declared context.
List<int> buildEmptyListFromContext() {
  final List<int> list = [];
  return list;
}

/// A heterogeneous literal with no explicit type argument or context: the
/// element type is inferred as the least upper bound of its elements'
/// static types.
final List<Object> heterogeneousList = [1, 'two', 3.0];

/// A const collection is unmodifiable at runtime: the analyzer accepts the
/// mutating call (the variable's static type is plain `List<int>`), but the
/// runtime call throws `UnsupportedError`.
String describeUnmodifiableConstCollection() {
  final list = const [1, 2, 3];
  try {
    list.add(4);
    return 'no-error';
  } on UnsupportedError catch (error) {
    return 'caught ${error.runtimeType}';
  }
}

/// Spread inference: the outer list literal's element type is inferred from
/// the spread source (`explicitTypedList`, a `List<int>`) rather than from
/// the trailing literal elements alone.
final List<int> spreadInferredList = [...explicitTypedList, 4, 5];

List<String> describeCollectionLiteralKindsAndInference() {
  return <String>[
    'explicitTypedList=$explicitTypedList',
    'contextuallyTypedList=${buildContextuallyTypedList()}',
    'constList=$constList',
    'explicitTypedSet=$explicitTypedSet',
    'contextuallyTypedSet=${buildContextuallyTypedSet()}',
    'constSet=$constSet',
    'explicitTypedMap=$explicitTypedMap',
    'contextuallyTypedMap=${buildContextuallyTypedMap()}',
    'constMap=$constMap',
    'defaultBraceLiteral=$defaultBraceLiteral (${defaultBraceLiteral.runtimeType})',
    'emptyListFromContext=${buildEmptyListFromContext()}',
    'heterogeneousList=$heterogeneousList (${heterogeneousList.runtimeType})',
    'unmodifiableConstCollection=${describeUnmodifiableConstCollection()}',
    'spreadInferredList=$spreadInferredList',
  ];
}
