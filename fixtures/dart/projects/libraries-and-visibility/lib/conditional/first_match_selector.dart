library;

// Two branches share the same `dart.library.io` condition. Conditional
// import/export selection uses the first matching condition, so
// `platform_native.dart` wins whenever `dart.library.io` is true;
// `platform_native_alt.dart` is never selected here.
import 'platform_default.dart'
    if (dart.library.io) 'platform_native.dart'
    if (dart.library.io) 'platform_native_alt.dart'
    as firstMatch;

String describeFirstMatchSelection() => firstMatch.platformLabel();
