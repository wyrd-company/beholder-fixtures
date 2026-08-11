import 'dart:io';

import 'package:configuration_and_versions/assertions/checks.dart';
import 'package:configuration_and_versions/environment/compile_time.dart';
import 'package:configuration_and_versions/language/legacy_consumer.dart';
import 'package:configuration_and_versions/language/post_super_params.dart';
import 'package:configuration_and_versions/language/pre_super_params.dart';
import 'package:configuration_and_versions/language/versioned_library.dart';
import 'package:configuration_and_versions/sdk_pin.dart';

void main(List<String> arguments) {
  final expectAssertions = arguments.contains('--expect-asserts');
  final assertionsRan = runAssertionProbe();
  if (assertionsRan != expectAssertions) {
    stderr.writeln(
      'unexpected assertion mode: ran=$assertionsRan expected=$expectAssertions',
    );
    exit(1);
  }

  final pair = pairFromOrigin();
  final holder = CounterHolder()..tally = pair.first;
  final bumped = bumpCounter(holder);

  final legacyTotal = ForwardedValue(2).number + SuperForwardedSlot(3).number;
  if (legacyTotal != 5) {
    stderr.writeln('unexpected legacy total: $legacyTotal');
    exit(1);
  }

  stdout.writeln(
    'vm-jit $pinnedSdkLowerBound $selectedSdkVersion '
    'pair=(${pair.first},${pair.second}) bump=$bumped ${environmentSummary()}',
  );
}
