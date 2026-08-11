/// Fixable use of a deprecated API for DART-CAN-DIAG-007.
///
/// This file represents the preview state before an automated fix is applied.
/// It deliberately calls the deprecated `helperLegacy` from the helper package.
/// A tool's `dart fix --dry-run` will report the fix supplied by the helper
/// package's `fix_data.yaml`, while `dart fix --apply` would rewrite it to
/// `helperNew` (see `deprecated_fixed.dart`).
library;

import 'package:helper/helper.dart';

// Fixable use: deprecated member from helper package.
String useDeprecated() => helperLegacy('d-1');

// Observation: data-driven fix metadata is supplied by the helper package
// (`packages/helper/lib/fix_data.yaml`). The preview versus applied
// distinction is demonstrated by comparing this file (preview) with
// `deprecated_fixed.dart` (applied).
