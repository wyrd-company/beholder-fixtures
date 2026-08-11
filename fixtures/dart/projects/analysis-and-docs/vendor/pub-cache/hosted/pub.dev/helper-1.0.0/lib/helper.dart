library;

import 'src/internal_registry.dart';
export 'src/deprecated_helper.dart';

/// Public helper that uses its package-internal registry compliantly
/// within the same package (library boundary internal to package).
class HelperFacade {
  const HelperFacade();

  void doWork() {
    const registry = HelperRegistry();
    registry.register('h-1');
  }
}

/// Demonstrates @internal visibility within package.
/// Violating use from outside package (e.g., `analysis_and_docs` importing
/// `HelperRegistry`) is not included as valid source and is recorded as
/// observation.
