/// Behavior shared by the VM JIT and native AOT entry points
/// (`bin/vm_main.dart`, `bin/native_aot_main.dart`), matching
/// DART-CAN-PLAT-003's same-behavior-in-JIT-and-AOT requirement: both
/// entry points call [runNativeChecks] and produce the same output shape.
library;

import 'dart:ffi' show sizeOf;

import '../diagnostics/non_portable_observations.dart';
import '../platform/platform_report.dart';
import '../platform/pragma_catalog.dart';
import '../platform/reachability.dart';
import 'native_bindings.dart';
import 'native_callback.dart';
import 'native_memory.dart';
import 'process_environment.dart';

/// Runs the platform, reachability, pragma, FFI, and process/filesystem
/// checks shared by every native (VM JIT and native AOT) entry point.
Future<void> runNativeChecks() async {
  print(buildPlatformReport());
  print(describeReachability());
  print('pragmaExamples=${combinePragmaExamples(2, 3)}');

  final scratch = nativeMalloc(sizeOf<Timespec>()).cast<Timespec>();
  print('wallClockSeconds=${currentWallClockSeconds(scratch)}');
  nativeFree(scratch.cast());

  print('sqrt(81)=${nativeSqrt(81.0)}');
  print('sorted=${sortInt32Buffer([5, 3, 4, 1, 2])}');

  final buffer = NativeBuffer(16);
  buffer.releaseNow();

  final scratchFileContents = await writeReadDeleteScratchFile(
    'platforms-and-interop',
  );
  print('scratchFileContents=$scratchFileContents');
  print('echoExitCode=${await runEchoProcess('platforms-and-interop')}');
  print('hasPathEnv=${readEnvironmentVariable('PATH') != null}');

  print(
    'runtimeTypeObservation='
    '${NonPortableObservations.runtimeTypeObservation(42)}',
  );
}
