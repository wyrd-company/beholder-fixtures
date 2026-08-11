/// DART-CAN-NULL-003: definite assignment and `late`.
library;

/// Local, path-complete assignment: `result` is definitely assigned on every
/// path through the `if`/`else`, so no `late` and no initializer are needed.
int describePathCompleteLocal(bool flag) {
  final int result;
  if (flag) {
    result = 1;
  } else {
    result = 2;
  }
  return result;
}

/// Top-level, path-complete assignment: reached the same way, at library
/// scope instead of inside a function body.
final int _pathCompleteTopLevelFlag = DateTime.now().microsecondsSinceEpoch;
final int pathCompleteTopLevel = _pathCompleteTopLevelFlag >= 0 ? 10 : 20;

int _topLevelInitCount = 0;

/// Top-level `late final` with a lazy initializer: `_computeTopLevelLazy`
/// runs only the first time `topLevelLazy` is read.
int _computeTopLevelLazy() {
  _topLevelInitCount += 1;
  return 42;
}

late final int topLevelLazy = _computeTopLevelLazy();

/// Static case: a lazily-initialized `late final` static field.
class StaticRegistry {
  static int staticInitCount = 0;

  static String _computeStaticLazy() {
    staticInitCount += 1;
    return 'registry-static';
  }

  static late final String staticLazy = _computeStaticLazy();
}

/// Instance case: an instance `late final` field with no initializer,
/// definitely assigned by a method rather than the constructor.
class ConfigurableWidget {
  late final String label;

  void configure(String value) {
    label = value;
  }
}

/// Instance case: an instance `late final` field with a lazy per-instance
/// initializer expression.
class LazyCache {
  int computeCount = 0;

  int _compute() {
    computeCount += 1;
    return 99;
  }

  late final int expensiveValue = _compute();
}

/// Constructor path: the `late final` field is definitely assigned in the
/// constructor body (not the initializer list), which is a valid
/// constructor path distinct from an initializing formal.
class DerivedFromBase {
  final int base;
  late final int derived;

  DerivedFromBase(this.base) {
    derived = base * 2;
  }
}

/// Constructor path: an ordinary (non-`late`) final field, definitely
/// assigned in the initializer list across a conditional expression.
class BranchedLabel {
  final String label;

  BranchedLabel(bool flag) : label = flag ? 'yes' : 'no';
}

/// Local case: a local `late` variable, lazily assigned by imperative code
/// before being read.
String describeLocalLate() {
  late String value;
  value = 'assigned-locally';
  return value;
}

/// A runtime read before `late` initialization throws `LateInitializationError`
/// (a subtype of `Error`), which is caught and reported here as a runtime
/// observation.
class NeverConfigured {
  late final String value;
}

String describeReadBeforeInitialization() {
  final holder = NeverConfigured();
  try {
    return 'value=${holder.value}';
  } on Error catch (error) {
    return 'caught ${error.runtimeType}';
  }
}

/// A second write to a `late final` field throws `LateInitializationError` at
/// runtime; the first write succeeds and the second is caught.
String describeSecondLateFinalWrite() {
  final widget = ConfigurableWidget();
  widget.configure('first');
  try {
    widget.configure('second');
    return 'label=${widget.label}';
  } on Error catch (error) {
    return 'first=${widget.label} caught ${error.runtimeType}';
  }
}

/// A `late final` initializer that throws is caught by the reader; the field
/// remains uninitialized and a later read re-attempts the same initializer.
class RiskyInitializer {
  int attempts = 0;

  int _computeRisky() {
    attempts += 1;
    throw StateError('initializer failure on attempt $attempts');
  }

  late final int riskyValue = _computeRisky();
}

String describeInitializerException() {
  final instance = RiskyInitializer();
  try {
    return 'value=${instance.riskyValue}';
  } on StateError catch (error) {
    return 'caught: ${error.message} (attempts=${instance.attempts})';
  }
}

List<String> describeDefiniteAssignmentAndLate() {
  return <String>[
    'pathCompleteLocal(true)=${describePathCompleteLocal(true)}',
    'pathCompleteLocal(false)=${describePathCompleteLocal(false)}',
    'pathCompleteTopLevel=$pathCompleteTopLevel',
    'topLevelLazy=$topLevelLazy initCount=$_topLevelInitCount',
    'staticLazy=${StaticRegistry.staticLazy} initCount=${StaticRegistry.staticInitCount}',
    'lazyCache=${LazyCache().expensiveValue}',
    'derivedFromBase=${DerivedFromBase(5).derived}',
    'branchedLabel=${BranchedLabel(true).label}',
    'localLate=${describeLocalLate()}',
    'readBeforeInit=${describeReadBeforeInitialization()}',
    'secondLateFinalWrite=${describeSecondLateFinalWrite()}',
    'initializerException=${describeInitializerException()}',
  ];
}
