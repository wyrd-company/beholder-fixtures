/// DART-CAN-NULL-002: flow promotion.
library;

/// Promotion through a null-check test (`!= null`).
String describeTestPromotion(String? input) {
  if (input != null) {
    return input.toUpperCase(); // input promoted to String
  }
  return 'null';
}

/// Promotion through an `== null` check paired with an early return.
String describeNullCheckReturn(String? input) {
  if (input == null) {
    return 'null';
  }
  return input.toUpperCase(); // input promoted after the guard clause
}

/// Promotion through a `throw` in the null branch.
String describeThrowPromotion(String? input) {
  if (input == null) {
    throw StateError('missing input');
  }
  return input.toUpperCase(); // input promoted after the throwing branch
}

/// Promotion through an assignment of a non-nullable value.
String describeAssignmentPromotion(String? input) {
  String? value = input;
  value = value ?? 'fallback';
  return value.toUpperCase(); // value promoted by the non-null assignment
}

/// Promotion through a null-check pattern (`if (... case final x?)`).
String describePatternPromotion(String? input) {
  if (input case final value?) {
    return value.toUpperCase(); // value bound and promoted by the pattern
  }
  return 'null';
}

/// Promotion carried independently down both branches of an `if`/`else`.
String describeBranchPromotion(String? input) {
  if (input == null) {
    return 'null';
  } else {
    return input.toUpperCase(); // promoted in the else branch
  }
}

/// A class with an eligible private final field: promotable because it is
/// both private and final.
class PromotableHolder {
  final String? _label;

  const PromotableHolder(this._label);

  String describe() {
    if (_label != null) {
      return _label.toUpperCase(); // private final field promoted
    }
    return 'none';
  }
}

/// A non-final field is never promotable; the null check narrows the read
/// only through a local copy or a null-assertion, not through field
/// promotion.
class MutableFieldHolder {
  String? label;

  MutableFieldHolder(this.label);

  String describe() {
    if (label != null) {
      // `label` stays `String?` here because non-final fields cannot be
      // promoted, so a null-assertion is required even under the guard.
      return label!.toUpperCase();
    }
    return 'none';
  }
}

/// A public field is never promotable, regardless of finality; only
/// `_privateFinal` (private and final) would be eligible.
class PublicFieldHolder {
  final String? publicLabel;

  const PublicFieldHolder(this.publicLabel);

  String describe() {
    if (publicLabel != null) {
      // `publicLabel` stays `String?` here because public fields are not
      // promotable even when final.
      return publicLabel!.toUpperCase();
    }
    return 'none';
  }
}

/// A getter of the same name declared on a subtype defeats promotion of the
/// base's private final field, because the flow analysis cannot tell which
/// declaration a subtype instance will resolve at the access site.
class ConflictingGetterBase {
  final String? _value;

  const ConflictingGetterBase(this._value);

  String describe() {
    if (_value != null) {
      // `_value` stays `String?` here: `ConflictingGetterSub` below
      // re-declares `_value` as a getter, so the field is not promotable on
      // this type hierarchy.
      return _value!.toUpperCase();
    }
    return 'none';
  }
}

class ConflictingGetterSub extends ConflictingGetterBase {
  const ConflictingGetterSub() : super(null);

  @override
  String? get _value => 'from-getter';
}

/// A class overriding `noSuchMethod` defeats private final field promotion,
/// because dynamic dispatch through `noSuchMethod` could intercept the
/// field access.
class NoSuchMethodHolder {
  final String? _value;

  const NoSuchMethodHolder(this._value);

  @override
  dynamic noSuchMethod(Invocation invocation) => super.noSuchMethod(invocation);

  String describe() {
    if (_value != null) {
      // `_value` stays `String?` here because this class overrides
      // `noSuchMethod`.
      return _value!.toUpperCase();
    }
    return 'none';
  }
}

/// Promotion defeated by reassignment (mutation) within the same guarded
/// scope: the later assignment gives `input` back its declared nullable
/// type for any code that follows it.
String describeMutationDefeat(String? input, String? Function() reload) {
  if (input != null) {
    final promotedLength = input.length; // still promoted here
    input = reload(); // mutation defeats promotion from this point on
    // `input` is `String?` again after the mutation.
    return 'len=$promotedLength next=${input?.toUpperCase() ?? 'null'}';
  }
  return 'null';
}

/// Promotion defeated by closure capture: a nested closure that assigns to
/// the captured variable prevents promotion of that variable anywhere in
/// the enclosing function, because the closure could run at any time.
String describeCaptureDefeat(String? input) {
  String? captured = input;
  void resetIfNeeded() {
    captured = null; // assigning inside a closure defeats promotion
  }

  if (captured != null) {
    resetIfNeeded();
    // `captured` stays `String?` here because it is captured and mutated by
    // `resetIfNeeded`.
    return captured?.toUpperCase() ?? 'reset-to-null';
  }
  return 'null';
}

/// Promotion defeated by a loop: promotion established *before* a loop does
/// not carry into the loop body when the body reassigns the variable,
/// because a later iteration could reach the same program point already
/// reassigned.
String describeLoopDefeat(String? seed, List<String?> updates) {
  String? current = seed;
  if (current == null) {
    return 'null';
  }
  // `current` is promoted to `String` at this point, before the loop.
  final observed = <String>[];
  for (final update in updates) {
    // `current` stays `String?` here, inside the loop body, because the
    // loop reassigns it below; a null-aware access is required even though
    // `current` was promoted just above the loop.
    observed.add(current?.toUpperCase() ?? 'null');
    current = update;
  }
  return observed.join(',');
}

/// The pre-field-promotion language-version variant lives in its own
/// library, `legacy_field_promotion.dart`, since a language-version override
/// applies per-library rather than per-declaration.
List<String> describeFlowPromotion() {
  return <String>[
    'test=${describeTestPromotion('alpha')}',
    'nullCheckReturn=${describeNullCheckReturn(null)}',
    'throwPromotion=${describeThrowPromotion('beta')}',
    'assignment=${describeAssignmentPromotion(null)}',
    'pattern=${describePatternPromotion('gamma')}',
    'branch=${describeBranchPromotion('delta')}',
    'promotableField=${const PromotableHolder('epsilon').describe()}',
    'mutableField=${MutableFieldHolder('zeta').describe()}',
    'publicField=${const PublicFieldHolder('eta').describe()}',
    'conflictingGetter=${const ConflictingGetterSub().describe()}',
    'noSuchMethodHolder=${const NoSuchMethodHolder('theta').describe()}',
    'mutationDefeat=${describeMutationDefeat('iota', () => null)}',
    'captureDefeat=${describeCaptureDefeat('kappa')}',
    'loopDefeat=${describeLoopDefeat('lambda', <String?>['mu', null, 'nu'])}',
  ];
}
