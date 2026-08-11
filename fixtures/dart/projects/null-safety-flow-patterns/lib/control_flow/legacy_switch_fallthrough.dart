// @dart=2.19

/// DART-CAN-FLOW-001: pre-Dart-3 switch fall-through rules. This library is
/// pinned below the Dart 3.0 language version, so its switch statement can
/// only use the classic constant-case forms: empty-case grouping and an
/// explicit labeled `continue` for fall-through. Pattern cases, guards, and
/// switch expressions all require Dart 3.0+ and are unavailable here; the
/// default-language-version library `switch_forms.dart` demonstrates the
/// post-Dart-3 pattern-based forms built on top of this same fall-through
/// mechanism.
library;

String describeLegacySwitchFallthrough(int value) {
  switch (value) {
    case 1:
    case 2:
      continue smallGroup;
    smallGroup:
    case 3:
      return 'small-group';
    default:
      return 'other';
  }
}
