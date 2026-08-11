@WorkshopTag('library-tag')
@Audited()
library;

@WorkshopTag('directive-tag')
import '../shared_models.dart';

import 'annotations.dart';

// Const-variable reference for annotation arguments.
const String defaultWorkshop = 'main-workshop';
const WorkshopTag workshopConst = WorkshopTag(defaultWorkshop);

/// Demonstrates metadata on a type.
@WorkshopTag('type-tag')
@Audited()
@WorkshopNote('first-note')
@WorkshopNote('second-note')
@Labeled<CatalogItem>('catalog-annotation')
class AnnotatedBin {
  const AnnotatedBin(this.name);

  @WorkshopTag('field-tag')
  final String name;

  @WorkshopTag('member-tag')
  @Audited()
  String describe() => 'bin:$name';
}

typedef TaggedItems = List<CatalogItem>;

/// Function with annotations on itself, parameters, and type parameters.
@WorkshopTag('function-tag')
@Audited()
T annotatedFunction<T extends CatalogItem>(
  @WorkshopTag('param-tag') T item,
  @WorkshopTag('param-tag-2') String label,
) {
  return item;
}

/// Annotation on type parameter.
class Holder<@WorkshopTag('type-param-tag') T> {
  const Holder(this.value);
  final T value;
}

/// Parameter example (not type-use).
CatalogItem? findItem(List<CatalogItem> items) =>
    items.isEmpty ? null : items.first;

/// Type-use: annotation on the `CatalogItem` type itself.
@WorkshopTag('type-use')
CatalogItem? typeUseExample;

/// Type-use on a field's type.
class TypeUseHolder {
  @WorkshopTag('type-use-field')
  CatalogItem held = const CatalogItem('u', 'v', 1);
}

/// Variable with metadata.
@WorkshopTag('variable-tag')
@Audited()
const WorkshopTag topLevelTaggedValue = workshopConst;

/// Generic annotation use if supported: @Labeled<CatalogItem>('example') already
/// demonstrated on [AnnotatedBin]. Repeated annotations shown there as well.
///
/// All targets from DART-CAN-DIAG-005 are covered:
/// library, directive, type, member, parameter, type parameter, variable,
/// and type use, plus const-variable reference, repeated, and generic.
