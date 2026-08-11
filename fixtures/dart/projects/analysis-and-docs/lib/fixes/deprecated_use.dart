/// Fixable use of a deprecated API for DART-CAN-DIAG-007.
///
/// This file represents the preview state before an automated fix is applied.
/// It deliberately calls the deprecated [legacyCreateItem]. A tool's
/// `dart fix --dry-run` would report the fix, while `dart fix --apply`
/// would rewrite it to the replacement API (see `deprecated_fixed.dart`).
library;

import '../shared_models.dart';
import 'deprecated_api.dart';

// Fixable use: deprecated member.
CatalogItem useDeprecated() => legacyCreateItem('d-1', 'Bracket');

// Observation: data-driven fix metadata is supplied only where the library
// authors it. This fixture's library does not ship additional `fix_data.yaml`
// beyond the `@deprecated` annotation itself. The preview versus applied
// distinction is demonstrated by comparing this file (preview) with
// `deprecated_fixed.dart` (applied).
