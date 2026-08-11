/// DART-CAN-COLL-003: null-aware collection elements.
library;

/// A null-eliding element (`?value`) in a list literal: included only when
/// non-null.
List<int> buildNullElidingList(int? first, int? second) => <int>[
  ?first,
  ?second,
  3,
];

/// A null-eliding element in a set literal.
Set<int> buildNullElidingSet(int? first, int? second) => <int>{
  ?first,
  ?second,
  3,
};

/// A null-eliding map key (`?key: value`): the whole entry is skipped when
/// the key is null.
Map<String, int> buildNullElidingKeyMap(String? key) => <String, int>{
  ?key: 1,
  'always': 2,
};

/// A null-eliding map value (`key: ?value`): the entry is skipped when the
/// value is null.
Map<String, int> buildNullElidingValueMap(int? value) => <String, int>{
  'maybe': ?value,
  'always': 2,
};

/// Contrast with nullable inclusion: without the `?` prefix, a nullable
/// element is included as an actual `null` entry, so the literal's element
/// type must itself be nullable (`List<int?>`).
List<int?> buildNullableInclusionList(int? first, int? second) => <int?>[
  first,
  second,
  3,
];

/// Interaction with spreads: a null-eliding element alongside a null-aware
/// spread (`...?`) in the same list literal.
List<int> buildNullElidingWithSpread(int? single, List<int>? spread) => <int>[
  ?single,
  ...?spread,
  99,
];

/// Interaction with control flow: a null-eliding element nested inside a
/// `for` loop over a list of nullable values.
List<int> buildNullElidingWithForLoop(List<int?> values) => <int>[
  for (final v in values) ?v,
];

/// Side-effect evaluation: a null-eliding element's expression is always
/// evaluated exactly once, whether or not the result turns out to be
/// null — evaluation determines inclusion, so it cannot itself be skipped
/// (unlike `??`, which skips evaluating its right-hand side entirely when
/// the left-hand side is already non-null).
final List<String> nullAwareElementSideEffectLog = <String>[];

int? _loggedNullableValue(String label, int? value) {
  nullAwareElementSideEffectLog.add('evaluate:$label');
  return value;
}

List<int> buildSideEffectingNullElidingList(int? present, int? absent) {
  nullAwareElementSideEffectLog.clear();
  return <int>[
    ?_loggedNullableValue('present', present),
    ?_loggedNullableValue('absent', absent),
  ];
}

List<String> describeNullAwareCollectionElements() {
  return <String>[
    'nullElidingList(both)=${buildNullElidingList(1, 2)}',
    'nullElidingList(one-null)=${buildNullElidingList(1, null)}',
    'nullElidingSet(one-null)=${buildNullElidingSet(1, null)}',
    'nullElidingKeyMap(present)=${buildNullElidingKeyMap('k')}',
    'nullElidingKeyMap(null)=${buildNullElidingKeyMap(null)}',
    'nullElidingValueMap(present)=${buildNullElidingValueMap(5)}',
    'nullElidingValueMap(null)=${buildNullElidingValueMap(null)}',
    'nullableInclusionList=${buildNullableInclusionList(1, null)}',
    'nullElidingWithSpread=${buildNullElidingWithSpread(null, <int>[7, 8])}',
    'nullElidingWithForLoop=${buildNullElidingWithForLoop(<int?>[1, null, 3])}',
    'sideEffectingNullElidingList=${buildSideEffectingNullElidingList(1, null)} log=$nullAwareElementSideEffectLog',
  ];
}
