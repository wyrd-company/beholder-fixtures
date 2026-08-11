import 'package:configuration_and_versions/environment/compile_time.dart';
import 'package:configuration_and_versions/sdk_pin.dart';

void main() {
  // The analyzer keeps [fixtureString] at its default while `dart compile js -D`
  // bakes the supplied value into the compiled program.
  print('js $pinnedSdkLowerBound flag=$fixtureString ${environmentSummary()}');
}
