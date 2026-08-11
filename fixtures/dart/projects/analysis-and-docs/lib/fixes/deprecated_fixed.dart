/// Applied-fix counterpart for DART-CAN-DIAG-007.
///
/// This file shows the state after the automated fix has been applied.
/// The deprecated call has been rewritten to the current API.
library;

import '../shared_models.dart';
import 'deprecated_api.dart';

CatalogItem useMigrated() => createItem('d-1', 'Bracket', quantity: 1);
