import 'dart:io';

import 'package:configuration_and_versions/assertions/checks.dart';
import 'package:configuration_and_versions/environment/compile_time.dart';
import 'package:configuration_and_versions/language/legacy_consumer.dart';
import 'package:configuration_and_versions/sdk_pin.dart';

void main() {
  final assertionsRan = runAssertionProbe();
  final pair = pairFromOrigin();

  stdout.writeln(
    'native-aot $pinnedSdkLowerBound assertions=$assertionsRan '
    'pair=(${pair.first},${pair.second}) ${environmentSummary()}',
  );
}
