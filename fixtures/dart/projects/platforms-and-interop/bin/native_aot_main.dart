/// The native AOT entry point, compiled with `dart compile exe` and then
/// executed. Calls the same [runNativeChecks] as `bin/vm_main.dart`,
/// demonstrating DART-CAN-PLAT-003's same-behavior-in-JIT-and-AOT
/// requirement, and is itself DART-CAN-PLAT-001's native-AOT cell of the
/// compilation-target matrix.
library;

import 'package:platforms_and_interop/native/common_checks.dart';

Future<void> main() async {
  await runNativeChecks();
  print('native-aot platforms-and-interop checks passed');
}
