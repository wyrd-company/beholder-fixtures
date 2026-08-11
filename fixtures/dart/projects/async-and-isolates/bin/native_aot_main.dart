import 'dart:io';

import 'package:async_and_isolates/isolates/isolate_checks.dart';

/// Drives isolate spawning and messaging under ahead-of-time
/// compilation. `Isolate.spawnUri` is not exercised here: an
/// AOT-compiled executable has no source compiler available to load a
/// sibling script by URI, so that variant is covered only on `vm-jit`
/// (see `bin/vm_main.dart`).
Future<void> main() async {
  await runIsolateSpawningChecks();
  await runSendableDataChecks();
  stdout.writeln('native-aot async-and-isolates checks passed');
}
