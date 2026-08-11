/// Demonstrates a compiler-accepted, analyzer-only violation.
///
/// The linter rule `non_constant_identifier_names` is enabled in
/// `analysis_options.yaml`. The declaration below violates that lint but is
/// still valid Dart and compiles without error. The analyzer reports the lint
/// while the compiler accepts the program.
library;

// ignore_for_file: avoid_print

// Analyzer-only violation: non-constant identifier names.
// ignore: non_constant_identifier_names
final my_Violating_Field = 42;

void useViolatingField() {
  print(my_Violating_Field);
}
