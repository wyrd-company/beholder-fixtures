/// Package-boundary internal API for contract demonstrations.
///
/// This library exposes members annotated with `package:meta` contracts that
/// are intended for use within the package but not outside it. The main
/// contracts library imports this file across a library boundary.
library;

import 'package:meta/meta.dart';

/// Intended for package-internal use only.
@internal
class InternalWorkshopRegistry {
  const InternalWorkshopRegistry();

  @internal
  void registerItem(String id) {}
}

/// Visible for testing only; not part of the public API.
@visibleForTesting
class TestHelper {
  const TestHelper();

  @visibleForTesting
  String debugLabel() => 'test-helper';
}
