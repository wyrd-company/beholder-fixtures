/// A documented workshop inventory library exercising dartdoc features.
///
/// This library demonstrates `///` docs, block docs, bracket references,
/// private references, imported and prefixed references, `@docImport`,
/// `@nodoc`, and doc-only dependencies for DART-CAN-DIAG-004.
///
/// References:
/// - Local type [CatalogItem]
/// - Private helper [_PrivateHelper]
/// - Imported type [Catalog] via `documentation/catalog.dart`
/// - Prefixed type [shared.CatalogItem] via `shared` prefix
/// - Record helper [makeRecord]
library;

/// @docImport 'dart:async';
/// @docImport '../shared_models.dart';
import '../shared_models.dart' as shared;
import '../shared_models.dart';
import 'catalog.dart';

// Doc-only dependency: used only in documentation, not in code.
/// See [Catalog] for an imported example that is also a code dependency.
/// See [Future] for a doc-only reference with no code import of `dart:async`.
// ignore: unused_import
// The import below is intentionally doc-only and not otherwise referenced.
// ignore: unused_import
import 'dart:async' as _docOnlyFutureImport;

/// Documents the workshop inventory with bracket references.
///
/// Links:
/// - [CatalogItem] is a local type.
/// - [_PrivateHelper] is a private type.
/// - [Catalog] is imported from `catalog.dart`.
/// - [shared.CatalogItem] is a prefixed reference.
/// Use [makeRecord] for a record-returning helper.
class DocumentedInventory {
  const DocumentedInventory(this.items);

  final List<CatalogItem> items;

  /// Returns the first item or `null` when empty.
  ///
  /// See also [CatalogItem.describe] and [_PrivateHelper].
  CatalogItem? firstItem() => items.isEmpty ? null : items.first;

  /// Creates a summary record.
  ///
  /// The record `(String label, int count)` exposes synthetic getters.
  (String label, int count) makeRecord(CatalogItem item) =>
      (item.label, item.quantity);
}

/// Makes a record for documentation examples.
(String label, int count) makeRecord(CatalogItem item) =>
    (item.label, item.quantity);

/*
 * Block documentation with resolvable references.
 *
 * This block doc references [CatalogItem] and [DocumentedInventory.firstItem].
 * It also mentions [Catalog] from the imported library.
 */

/// This declaration is hidden from documentation.
///
/// @nodoc
class HiddenInternal {
  const HiddenInternal();
}

/// Public container that re-exports a doc-only versus code dependency contrast.
///
/// Code depends on [CatalogItem] via the `shared` prefix.
/// Docs also reference [Future] without a code dependency on `dart:async`
/// beyond the doc-only import above.
class DocContrast {
  const DocContrast();

  shared.CatalogItem makeItem(String id, String label) =>
      shared.CatalogItem(id, label, 1);
}
