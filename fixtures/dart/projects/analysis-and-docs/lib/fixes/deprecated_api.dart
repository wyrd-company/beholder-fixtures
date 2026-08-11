/// Deprecated API definitions for DART-CAN-DIAG-007.
library;

import '../shared_models.dart';

/// Previous API that has been superseded.
///
/// Migration: use [createItem] instead. A fix would rewrite `legacyCreateItem`
/// calls to `createItem`.
@deprecated
CatalogItem legacyCreateItem(String id, String label) =>
    CatalogItem(id, label, 1);

/// Current replacement API.
CatalogItem createItem(String id, String label, {int quantity = 1}) =>
    CatalogItem(id, label, quantity);
