/// Demonstrates suppression and generated markers for DART-CAN-DIAG-003.
library;

// File-wide ignore: suppresses `avoid_print` for the whole file.
// ignore_for_file: avoid_print, duplicate_ignore

import '../shared_models.dart';
import '../generated/sample_generated.dart';

// Uses a generated-marked library as a normal import to show it participates
// in the program despite the generated header and exclusions.
String useGenerated() => GeneratedSample.tag();

// Next-line ignore: suppresses the lint on the following line only.
void logWithNextLineIgnore() {
  // ignore: avoid_print, duplicate_ignore
  print('next-line ignored print');
}

// File-wide ignored lint: this print would otherwise trigger `avoid_print`
// but is suppressed by the `ignore_for_file` at the top.
void logWithFileIgnore() {
  print('file-wide ignored print');
}

// Suppressed lint versus unsuppressible language error (observation, not asserted):
//
// - `// ignore: avoid_print` suppresses the lint `avoid_print`.
// - `// ignore: syntax_error` does NOT suppress a language error. The source
//   remains valid here; the contrast is documented as an observation because
//   an actual syntax error would make the fixture invalid and is not included.
//   See DART-CAN-DIAG-003.
CatalogItem makeItem() => const CatalogItem('s-1', 'Bracket', 2);
