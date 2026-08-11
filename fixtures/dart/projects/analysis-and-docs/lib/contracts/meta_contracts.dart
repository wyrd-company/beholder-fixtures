/// Analyzer contract annotations via `package:meta` for DART-CAN-DIAG-006.
///
/// All uses are compliant. Violating uses are recorded as observations in
/// comments and are not asserted as fixture behavior.
library;

import 'package:meta/meta.dart';
import 'package:helper/helper.dart';

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

/// Package-boundary internal use within helper package.
/// `HelperFacade` uses `HelperRegistry` inside its own package compliantly.
void useHelperPackage() {
  const facade = HelperFacade();
  facade.doWork();
}

// Observation: calling `InternalWorkshopRegistry` from outside
// `analysis_and_docs` package or `HelperRegistry` from outside `helper`
// would be a violation of `@internal` and is not included.

/// Demonstrates `@visibleForTesting`: the member is intended for test access,
/// and a reference from within its own declaring library is compliant and
/// raises no `invalid_use_of_visible_for_testing_member` diagnostic.
class TestSeam {
  const TestSeam();

  @visibleForTesting
  int computeForTest() => 42;
}

/// Compliant use of a `@visibleForTesting` member from within its declaring
/// library. A use from outside this library (and outside a test) would violate
/// the contract and is recorded as an observation only.
int useVisibleForTestingWithinLibrary() => const TestSeam().computeForTest();

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

// Compliant use of `@useResult` consumes the result.
String consumeUseResult(CatalogItem item) => computeLabel(item).toUpperCase();

/// Demonstrates `@reopen` with a `final` supertype.
/// `ReopenBase` is `final`; this `base` subtype intentionally reopens the
/// final restriction and the annotation suppresses the `implicit_reopen` lint.
final class ReopenBase {
  void perform() {}
}

@reopen
base class Reopened extends ReopenBase {
  @override
  void perform() {}
}

/// Demonstrates `@redeclare` on an extension type member that redeclares a
/// superinterface member.
abstract class HasIdValue {
  int get idValue;
}

class IdHolder implements HasIdValue {
  const IdHolder(this.idValue);
  @override
  final int idValue;
}

extension type WorkshopId(IdHolder holder) implements HasIdValue {
  @redeclare
  int get idValue => holder.idValue;
}

/// Observation: violating cases such as omitting `super.dispose()` when
/// `@mustCallSuper` is required, ignoring a `@useResult` value, or overriding
/// a `@immutable` class with mutable fields are not represented as valid
/// source. They are recorded here as observations.
