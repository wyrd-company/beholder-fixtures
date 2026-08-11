/// DART-CAN-NULL-004: null-aware selection and fallback.
library;

/// A shared hop counter, used to observe exactly how many `.loggedNext`
/// getters run before a `?.` chain short-circuits.
int chainGetterHops = 0;

class Chain {
  final Chain? next;
  final int? payload;

  Chain({this.next, this.payload});

  /// A getter with a side effect, used to observe whether a `?.` chain
  /// short-circuits evaluation once an intermediate link is null.
  Chain? get loggedNext {
    chainGetterHops += 1;
    return next;
  }
}

/// `?.` selection, including a multi-hop chain.
int? describeChainPayload(Chain? chain) => chain?.payload;

/// Whole-chain short-circuiting: the chain runs one `.loggedNext` hop per
/// present link, and stops the instant a hop returns null, so `payload` is
/// read only when every link up to it was present.
int? describeDeepChain(Chain? chain) => chain?.loggedNext?.loggedNext?.payload;

class ScoreBoard {
  final Map<String, int> scores;
  int? _lastLookup;

  ScoreBoard(this.scores);

  int? get lastLookup => _lastLookup;

  set lastLookup(int? value) {
    _lastLookup = value;
  }
}

/// Null-aware indexing read (`?[]`) on a nullable receiver.
int? describeIndexedRead(Map<String, int>? scores, String key) => scores?[key];

int sideEffectInvocations = 0;

int _recordSideEffect(int value) {
  sideEffectInvocations += 1;
  return value;
}

/// Side effects on the right-hand side of a null-aware property assignment
/// are skipped entirely when the receiver is null: `_recordSideEffect` never
/// runs for a null `board`.
void describeSkippedPropertyAssignment(ScoreBoard? board) {
  board?.lastLookup = _recordSideEffect(1);
}

/// Side effects on the right-hand side of a null-aware index assignment are
/// likewise skipped when the receiver map itself is null.
void describeSkippedIndexAssignment(Map<String, int>? scores) {
  scores?['bonus'] = _recordSideEffect(2);
}

/// `??` supplies a fallback only when the left operand is null.
int describeIfNullFallback(int? input) => input ?? -1;

int? _cachedTotal;

/// `??=` assigns only when the target is currently null, and only evaluates
/// its right-hand side in that case.
int describeCacheOrCompute(int Function() compute) {
  _cachedTotal ??= compute();
  return _cachedTotal!;
}

/// A `!` that is certain to succeed: `input` is non-null by the time this
/// runs.
int describeSuccessfulBang(int? input) => input!;

/// A `!` on a null value throws `TypeError` at runtime ("Null check operator
/// used on a null value"), caught and reported here.
String describePostfixBangFailure() {
  int? nothing;
  try {
    return 'value=${nothing!}';
  } on TypeError catch (error) {
    return 'caught ${error.runtimeType}';
  }
}

class Profile {
  String? _nickname;

  String? get nickname => _nickname;

  /// The setter trims and normalizes, so getter/setter interaction is
  /// observable: what is read back may differ from what was set.
  set nickname(String? value) {
    _nickname = value?.trim();
  }
}

/// Property getter/setter interaction through `?.`: the setter runs a
/// side-effecting normalization, and the getter reflects the normalized
/// value on the next read.
String describeGetterSetterInteraction(Profile? profile) {
  profile?.nickname = '  padded  ';
  return profile?.nickname ?? 'no-profile';
}

class Basket {
  final List<String> items = <String>[];

  void addItem(String item) {
    items.add(item);
  }
}

/// The cascade boundary: a leading `?..` null-shorts the whole cascade
/// (every following plain `..` section as well) when the receiver is null,
/// while a non-null receiver runs every section.
List<String> describeCascadeBoundary(Basket? basket) {
  basket
    ?..addItem('first')
    ..addItem('second');
  return basket?.items ?? const <String>[];
}

List<String> describeNullAwareSelection() {
  final chainOfTwo = Chain(payload: 5);
  final chainOfNull = Chain();

  chainGetterHops = 0;
  final fullDeepChain = Chain(next: Chain(next: Chain(payload: 9)));
  final deepChainResult = describeDeepChain(fullDeepChain);
  final hopsForFullChain = chainGetterHops;

  chainGetterHops = 0;
  describeDeepChain(null);
  final hopsForNullReceiver = chainGetterHops;

  chainGetterHops = 0;
  final midChainBreak = Chain(payload: 1);
  describeDeepChain(midChainBreak);
  final hopsForMidChainBreak = chainGetterHops;

  final populatedBoard = ScoreBoard(<String, int>{'alpha': 1});
  describeSkippedPropertyAssignment(null);
  final skippedAssignmentCount = sideEffectInvocations;
  describeSkippedIndexAssignment(null);
  final skippedIndexCount = sideEffectInvocations;

  return <String>[
    'chainPayload(present)=${describeChainPayload(chainOfTwo)}',
    'chainPayload(null-field)=${describeChainPayload(chainOfNull)}',
    'chainPayload(null-receiver)=${describeChainPayload(null)}',
    'deepChain(full)=$deepChainResult hops=$hopsForFullChain',
    'deepChain(null-receiver) hops=$hopsForNullReceiver',
    'deepChain(mid-break) hops=$hopsForMidChainBreak',
    'indexedRead(present)=${describeIndexedRead(<String, int>{'a': 3}, 'a')}',
    'indexedRead(null-receiver)=${describeIndexedRead(null, 'a')}',
    'skippedPropertyAssignmentSideEffects=$skippedAssignmentCount',
    'skippedIndexAssignmentSideEffects=$skippedIndexCount',
    'ifNullFallback(null)=${describeIfNullFallback(null)}',
    'ifNullFallback(7)=${describeIfNullFallback(7)}',
    'cacheOrCompute=${describeCacheOrCompute(() => 100)}',
    'cacheOrComputeCached=${describeCacheOrCompute(() => 200)}',
    'successfulBang=${describeSuccessfulBang(42)}',
    'postfixBangFailure=${describePostfixBangFailure()}',
    'getterSetterInteraction(present)=${describeGetterSetterInteraction(Profile())}',
    'getterSetterInteraction(null)=${describeGetterSetterInteraction(null)}',
    'cascadeBoundary(present)=${describeCascadeBoundary(Basket())}',
    'cascadeBoundary(null)=${describeCascadeBoundary(null)}',
    'scoreBoardLastLookup=${populatedBoard.lastLookup}',
  ];
}
