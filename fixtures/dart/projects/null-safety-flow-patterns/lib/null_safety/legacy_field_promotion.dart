// @dart=3.1

/// DART-CAN-NULL-002: a pre-field-promotion language version. Private final
/// field promotion is a Dart 3.2+ capability, so this library is pinned
/// below that version (`3.1`, still sound-null-safe) and relies on the
/// long-standing local-copy idiom instead of field promotion.
library;

class LegacyFieldHolder {
  final String? _label;

  const LegacyFieldHolder(this._label);

  String describe() {
    final label = _label; // local copy: the portable pre-3.2 idiom
    if (label != null) {
      return label
          .toUpperCase(); // the local variable is promoted, not the field
    }
    return 'none';
  }
}

String describeLegacyFieldPromotion() =>
    'legacyField=${const LegacyFieldHolder('legacy-value').describe()}';
