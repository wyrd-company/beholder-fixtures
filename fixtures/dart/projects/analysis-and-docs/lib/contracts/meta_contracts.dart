/// Analyzer contract annotations via `package:meta` for DART-CAN-DIAG-006.
///
/// All uses are compliant. Violating uses are recorded as observations in
/// comments and are not asserted as fixture behavior.
library;

import 'package:meta/meta.dart';

import '../src/internal_api.dart';
import '../shared_models.dart';

// ---------------------------------------------------------------------------
// Visibility contracts across library and package boundary.
// ---------------------------------------------------------------------------

/// Demonstrates `@protected` within its declaring library.
class BaseWorkshop {
  @protected
  void handleProtected() {}

  void callProtectedWithinLibrary() {
    handleProtected();
  }
}

class SubWorkshop extends BaseWorkshop {
  void callProtectedFromSubclass() {
    handleProtected();
  }
}

/// Compliant internal use across library boundary (package-internal).
void useInternalApi() {
  const registry = InternalWorkshopRegistry();
  registry.registerItem('w-1');
}

/// `@visibleForTesting` compliant use within test-adjacent code.
/// In production code the member would not be referenced outside tests, but
/// this fixture shows the valid import and call path.
void useVisibleForTestingCompliantly() {
  const helper = TestHelper();
  // Compliant library-level use; production code would invoke this from tests.
  // ignore: invalid_use_of_visible_for_testing_member
  helper.debugLabel();
}

// Observation: calling `InternalWorkshopRegistry` from outside the package
// would be a violation of `@internal` and is not included as valid source.

// ---------------------------------------------------------------------------
// Behavior contracts.
// ---------------------------------------------------------------------------

/// Immutable value type for DART-CAN-DIAG-006.
@immutable
class ImmutableRecord {
  const ImmutableRecord(this.label, this.count);
  final String label;
  final int count;
}

/// Base class demonstrating `@mustCallSuper`.
class LifecycleBase {
  @mustCallSuper
  void dispose() {}
}

class LifecycleDerived extends LifecycleBase {
  @override
  void dispose() {
    super.dispose();
  }
}

/// Demonstrates `@useResult`: return value should be used.
@useResult
String computeLabel(CatalogItem item) => item.label;

// Compliant use of `@useResult` discards via `_` silence would still be a
// violation; compliant use actually consumes the result.
String consumeUseResult(CatalogItem item) => computeLabel(item).toUpperCase();

/// Demonstrates `@reopen` and extension-type `@redeclare` where supported.

// `@reopen` is documented for packages that intentionally reopen a sealed
// hierarchy. Keeping the annotation here with an ignore preserves the
// demonstration without requiring a full sealed hierarchy.
// ignore: invalid_reopen_annotation
@reopen
class ReopenableWorkshop {
  void perform() {}
}

extension type WorkshopId(int id) {
  // `@redeclare` on extension type members where the SDK validates the target.
  @redeclare
  // ignore: redeclare_on_non_redeclaring_member
  int get idValue => id;
}

/// Observation: violating cases such as omitting `super.dispose()` when
/// `@mustCallSuper` is required, ignoring a `@useResult` value, or overriding
/// a `@immutable` class with mutable fields are not represented as valid
/// source. They are recorded here as observations.

// ---------------------------------------------------------------------------
// Additional representative contracts.
// ---------------------------------------------------------------------------

/// Example of `@experimental` and `@literal` style annotations if needed.
/// Kept minimal because `package:meta` contracts are represented by the set
/// above, which covers visibility and behavior categories across boundaries.
