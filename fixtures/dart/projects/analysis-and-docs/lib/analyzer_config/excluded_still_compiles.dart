/// File excluded from analysis via `analysis_options.yaml` but still compiled.
///
/// `analysis_options.yaml` contains an `analyzer.exclude` entry for this path.
/// The linter reports for this file are suppressed by exclusion, yet the
/// compiler still compiles it as part of the program. This demonstrates the
/// "excluded file still compiled" variant of DART-CAN-DIAG-002.
///
/// Despite being excluded from analysis, this file remains valid Dart.
library;

int excludedValue() => 7;

String describeExcluded() => 'excluded:$excludedValue';
