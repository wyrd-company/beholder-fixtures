/// The default VM JIT entry point (`dart run bin/vm_main.dart`), one cell
/// of DART-CAN-PLAT-001's compilation-target matrix.
library;

import 'package:platforms_and_interop/native/common_checks.dart';

Future<void> main() async {
  await runNativeChecks();
  print('vm-jit platforms-and-interop checks passed');
}
