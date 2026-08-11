/// Runtime observations that are valid to record but must never be
/// asserted for portable equality across compilation targets, matching
/// DART-CAN-PLAT-011. Each method documents why its result is
/// implementation-defined rather than a portable contract; none of them is
/// compared against an expected value anywhere in this project.
library;

final class NonPortableObservations {
  const NonPortableObservations._();

  /// The runtime type string of [value]. Its exact text differs between VM
  /// JIT, native AOT, and minified `js`/`wasm` output.
  static String runtimeTypeObservation(Object value) =>
      value.runtimeType.toString();

  /// A synthetic closure name. Anonymous functions and mixin applications
  /// receive backend-assigned synthetic names that are not stable across
  /// targets or minification settings.
  static String syntheticNameObservation() {
    String Function() closure = () => 'anonymous';
    return closure.runtimeType.toString();
  }

  /// A captured stack trace. Frame text, source positions, and inlining
  /// decisions vary by backend, optimization level, and source-map
  /// configuration.
  static String stackTraceObservation() {
    try {
      throw StateError('non-portable observation probe');
    } catch (_, stackTrace) {
      return stackTrace.toString();
    }
  }

  /// The message text of a thrown runtime error. Wording, formatting, and
  /// which details are included are backend-defined.
  static String errorMessageObservation() {
    try {
      final empty = <int>[];
      return empty[0].toString();
    } on RangeError catch (error) {
      return error.toString();
    }
  }

  /// An identity hash code. Allocation strategy, object layout, and hashing
  /// are backend-defined and unstable across runs and targets.
  static int hashObservation(Object value) => value.hashCode;

  /// Records that `platform/reachability.dart`'s `unreachableGreeting` is a
  /// tree-shaken-boundary observation: retained under VM JIT (which does
  /// not tree-shake), eligible for omission under native AOT, `js`, and
  /// `wasm`. This project does not assert which compiled binaries actually
  /// omit it.
  static const String treeShakenBoundaryNote =
      'platform/reachability.dart#unreachableGreeting is retained under '
      'VM JIT and eligible for tree shaking under native AOT, js, and wasm';
}
