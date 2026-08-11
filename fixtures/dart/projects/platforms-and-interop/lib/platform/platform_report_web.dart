/// The web-only half of DART-CAN-PLAT-002's conditional platform-library
/// isolation; selected by `platform_report.dart` when `dart:js_interop` is
/// available (`js` and `wasm`) instead of `platform_report_native.dart`.
library;

import 'dart:js_interop';

@JS('navigator.userAgent')
external JSString get _userAgent;

/// A capability report assembled from the web-only `dart:js_interop`
/// library. Its [toString] output is never asserted for portable equality
/// with `platform_report_native.dart`'s report: the two targets expose
/// entirely different platform capabilities, and this class exists only to
/// give `platform_report.dart` the same call shape on both branches.
final class PlatformReport {
  const PlatformReport({required this.userAgent});

  /// The JavaScript `navigator.userAgent`, read through an external `@JS`
  /// binding rather than a native platform library.
  final String userAgent;

  @override
  String toString() => 'web(userAgent: $userAgent)';
}

/// Builds a [PlatformReport] through the web-only `dart:js_interop`
/// binding this file declares.
PlatformReport buildPlatformReport() =>
    PlatformReport(userAgent: _userAgent.toDart);
