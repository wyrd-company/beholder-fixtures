/// DART-CAN-COLL-002: collection control flow and spreads.
library;

/// Collection `if`/`else` inside a list literal.
List<String> buildConditionalList(bool includeExtra) {
  return <String>['base', if (includeExtra) 'extra' else 'fallback'];
}

/// Collection `if-case` inside a list literal.
List<String> buildIfCaseList(Object? value) {
  return <String>['base', if (value case int n) 'int:$n'];
}

/// A `for` with a destructuring pattern, inside a list literal.
List<String> buildForPatternList(List<(String, int)> entries) {
  return <String>[for (final (name, count) in entries) '$name:$count'];
}

/// `...` spreads into a list, a set, and a map.
List<int> buildSpreadList(List<int> a, List<int> b) => <int>[...a, ...b];

Set<int> buildSpreadSet(Set<int> a, Set<int> b) => <int>{...a, ...b};

Map<String, int> buildSpreadMap(Map<String, int> a, Map<String, int> b) =>
    <String, int>{...a, ...b};

/// `...?` skips the whole spread when its source is null, in a list, a set,
/// and a map.
List<int> buildNullAwareSpreadList(List<int>? source) => <int>[
  0,
  ...?source,
  9,
];

Set<int> buildNullAwareSpreadSet(Set<int>? source) => <int>{0, ...?source, 9};

Map<String, int> buildNullAwareSpreadMap(Map<String, int>? source) =>
    <String, int>{'zero': 0, ...?source, 'nine': 9};

/// Nested collection control flow: a `for` containing a collection
/// `if`/`else`.
List<String> buildNestedForIfForms(List<int> values) => <String>[
  for (final v in values)
    if (v.isEven) 'even:$v' else 'odd:$v',
];

/// Nested collection control flow the other way: a collection `if`
/// containing a `for` (and its own nested spread).
List<int> buildNestedIfForForms(bool includeDoubled, List<int> values) => <int>[
  ...values,
  if (includeDoubled)
    for (final v in values) v * 2,
];

const List<int> _constBase = <int>[1, 2];

/// Const restrictions: a const collection literal may only spread other
/// compile-time-constant sources, such as this const list.
const List<int> constSpreadList = <int>[..._constBase, 3];

List<String> describeCollectionControlFlowAndSpreads() {
  return <String>[
    'conditionalList(true)=${buildConditionalList(true)}',
    'conditionalList(false)=${buildConditionalList(false)}',
    'ifCaseList(match)=${buildIfCaseList(5)}',
    'ifCaseList(no-match)=${buildIfCaseList('nope')}',
    'forPatternList=${buildForPatternList(const <(String, int)>[('a', 1), ('b', 2)])}',
    'spreadList=${buildSpreadList(const <int>[1, 2], const <int>[3, 4])}',
    'spreadSet=${buildSpreadSet(const <int>{1, 2}, const <int>{2, 3})}',
    'spreadMap=${buildSpreadMap(const <String, int>{'a': 1}, const <String, int>{'b': 2})}',
    'nullAwareSpreadList(present)=${buildNullAwareSpreadList(const <int>[4, 5])}',
    'nullAwareSpreadList(null)=${buildNullAwareSpreadList(null)}',
    'nullAwareSpreadSet(null)=${buildNullAwareSpreadSet(null)}',
    'nullAwareSpreadMap(null)=${buildNullAwareSpreadMap(null)}',
    'nestedForIfForms=${buildNestedForIfForms(const <int>[1, 2, 3, 4])}',
    'nestedIfForForms=${buildNestedIfForForms(true, const <int>[1, 2])}',
    'constSpreadList=$constSpreadList',
  ];
}
