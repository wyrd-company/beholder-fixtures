/// Demonstrates strict casts, inference, and raw-type handling under the
/// project's analyzer configuration (`analysis_options.yaml`).
library;

import '../shared_models.dart';

// Strict casts: explicit cast required when downcasting from dynamic.
int strictCastExample(dynamic value) {
  // Analyzer with strict-casts warns without an explicit `as`.
  final asInt = value as int;
  return asInt + 1;
}

// Strict inference: type is inferred without explicit annotation where allowed.
String strictInferenceExample() {
  var inferred = 'inferred-value';
  return inferred;
}

// Strict raw types: generic type arguments must be explicit.
List<CatalogItem> strictRawTypesExample(List<CatalogItem> items) {
  final explicit = <CatalogItem>[];
  explicit.addAll(items);
  return explicit;
}
