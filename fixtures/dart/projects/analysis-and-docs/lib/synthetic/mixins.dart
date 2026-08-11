/// Mixin application classes and named versus anonymous applications.
library;

mixin Sealable {
  String seal() => 'sealed';
}

mixin LabeledMixin {
  String labelOf(String s) => 'label:$s';
}

class BaseBin {
  String describe() => 'base';
}

// Anonymous mixin application: `BaseBin with Sealable` creates a synthetic
// intermediate class without a named declaration.
class WorkshopBin extends BaseBin with Sealable, LabeledMixin {
  WorkshopBin(this.id);
  final String id;
}

// Named mixin application: explicit class alias introduces a named application.
class NamedApp extends BaseBin with Sealable {}

mixin class MixedClass {
  String mixed() => 'mixed';
}

// Demonstrates that mixin application introduces observable `is` and `as`
// behavior via the synthetic intermediate.
bool isSealable(BaseBin bin) => bin is Sealable;

String useNamedMixins() {
  final a = NamedApp();
  final b = WorkshopBin('w-1');
  return '${a.describe()}:${b.seal()}';
}
