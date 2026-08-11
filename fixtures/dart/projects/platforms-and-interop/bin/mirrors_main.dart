/// A dedicated JIT-only entry point (`dart run bin/mirrors_main.dart`),
/// exercising DART-CAN-PLAT-009's reflective JIT-only source set. This
/// file is never passed to `dart compile exe`, `dart compile js`, or
/// `dart compile wasm`: `dart:mirrors` is rejected outright by native AOT,
/// `js`, and `wasm` compilation, so this project isolates it as an entry
/// point that is only ever run, not compiled to another target.
library;

import 'package:platforms_and_interop/reflect/reflective_registry.dart';

void main() {
  final target = ReflectiveTarget<int>(42);
  print(describeReflectively(target));
  print('mirrors-jit-only platforms-and-interop checks passed');
}
