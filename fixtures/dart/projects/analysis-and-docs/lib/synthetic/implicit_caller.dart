/// Cross-library implicit default-constructor invocation for DART-CAN-DIAG-008.
library;

import 'implicit_entities.dart';

/// Invokes the implicit default constructor of [ImplicitDefault] from a
/// different library than its declaration.
ImplicitDefault createCrossLibraryImplicit() => ImplicitDefault();
