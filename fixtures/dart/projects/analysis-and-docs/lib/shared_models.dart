/// Shared domain models used across documentation, metadata, and synthetic fixtures.
///
/// The theme is a small workshop inventory with generic, non-identifying values.
library;

// ignore_for_file: avoid_print

/// A catalog item tracked by the workshop.
class CatalogItem {
  const CatalogItem(this.id, this.label, this.quantity);

  final String id;
  final String label;
  final int quantity;

  String describe() => 'Item $label ($id) x$quantity';
}

/// A container holding workshop supplies.
class SupplyBin {
  SupplyBin(this.name, this.items);

  final String name;
  final List<CatalogItem> items;

  int totalQuantity() => items.fold(0, (sum, e) => sum + e.quantity);
}

/// Private helper used for documentation reference demonstrations.
class _PrivateHelper {
  const _PrivateHelper();

  String help() => 'private-helper';
}

/// Exposed helper that documents its private counterpart via bracket references.
class PublicFacade {
  const PublicFacade();

  /// Returns assistance from [_PrivateHelper].
  String assist() => const _PrivateHelper().help();
}

/// Simple value type used for record and accessor demonstrations.
class MeasuredValue {
  MeasuredValue(this.amount, this.unit);

  final double amount;
  final String unit;
}
