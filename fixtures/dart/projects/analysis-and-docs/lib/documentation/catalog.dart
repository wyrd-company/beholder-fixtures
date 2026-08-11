/// Supplementary catalog used for imported documentation references.
library;

import '../shared_models.dart';

/// A public inventory referenced from another library's docs.
class Catalog {
  const Catalog();

  /// Lists items in the workshop.
  List<CatalogItem> listItems() => const [];
}
