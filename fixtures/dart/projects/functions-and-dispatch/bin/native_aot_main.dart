import 'dart:io';

import 'package:functions_and_dispatch/checks/check_support.dart';
import 'package:functions_and_dispatch/dispatch/dispatch_resolution.dart';
import 'package:functions_and_dispatch/entrypoints/reachability.dart';
import 'package:functions_and_dispatch/types/tear_offs.dart';

/// Drives dispatch resolution, tear-off identity, and the
/// `vm:entry-point` reachability pragma under ahead-of-time
/// compilation, confirming the same outcomes as the `vm-jit` entry
/// libraries hold under `native-aot`.
void main() {
  const toolkit = MathToolkit(5);
  final tearOffComparison = compareTearOffs(toolkit);
  expectTrue(
    tearOffComparison.topLevelIdentical,
    'native-aot top-level tear-off identity',
  );
  expectTrue(
    tearOffComparison.staticIdentical,
    'native-aot static tear-off identity',
  );
  expectTrue(
    tearOffComparison.boundEqual,
    'native-aot bound tear-off equality',
  );

  expectEqual(
    virtualDispatch(Circle()),
    'circle',
    'native-aot virtualDispatch',
  );
  expectEqual(
    extensionDispatch(Circle()),
    'extension-shape:Circle',
    'native-aot extensionDispatch',
  );
  expectEqual(
    extensionTypeDispatch(Circle()),
    'view:circle',
    'native-aot extensionTypeDispatch',
  );

  expectEqual(
    dispatchByName('dynamic-only', 'x'),
    'handled:x',
    'native-aot dispatchByName reaches pragma-marked handler',
  );

  stdout.writeln('native-aot native_aot_main checks passed');
}
