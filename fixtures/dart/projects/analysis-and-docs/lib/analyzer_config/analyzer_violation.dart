/// Demonstrates a compiler-accepted, analyzer-only violation.
///
/// The linter rule `non_constant_identifier_names` is enabled in
/// `analysis_options.yaml`. The declaration below violates that lint but is
/// still valid Dart and compiles without error. The analyzer reports the lint
/// while the compiler accepts the program.
library;

// Analyzer-only violation: non-constant identifier names.
// The violation is observable via `dart analyze` as an info diagnostic
// `non_constant_identifier_names` on the following declaration, while
// `dart format` and `dart compile` succeed. No ignore is used so the
// diagnostic remains visible, yet `task lint` (which runs `dart analyze`)
// still passes because the diagnostic is info-level, not an error.
final my_Violating_Field = 42;

void useViolatingField() {
  // ignore: avoid_print
  print(my_Violating_Field);
}
