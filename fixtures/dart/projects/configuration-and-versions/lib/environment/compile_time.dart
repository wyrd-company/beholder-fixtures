/// Compile-time environment values for [DART-CAN-CFG-003].
library;

import 'package:configuration_and_versions/environment/platform_selector.dart';

/// String define with a default used by the analyzer when no `-D` is supplied.
const String fixtureString = String.fromEnvironment(
  'FIXTURE_STRING',
  defaultValue: 'analyzer-default',
);

/// Integer define with a default.
const int fixtureInt = int.fromEnvironment('FIXTURE_INT', defaultValue: 7);

/// Boolean define with a default.
const bool fixtureBool = bool.fromEnvironment(
  'FIXTURE_BOOL',
  defaultValue: false,
);

/// Whether the string define was supplied at compile time.
const bool hasFixtureString = bool.hasEnvironment('FIXTURE_STRING');

/// Whether an absent define is observable through [bool.hasEnvironment].
const bool hasFixtureMissing = bool.hasEnvironment('FIXTURE_MISSING');

/// Deployment label combined with conditional platform selection.
const String deploymentMode = String.fromEnvironment(
  'DEPLOY_MODE',
  defaultValue: 'local',
);

/// Summarizes compile-time environment and conditional-import selection.
String environmentSummary() {
  return '$fixtureString|$fixtureInt|$fixtureBool|'
      'hasString=$hasFixtureString|hasMissing=$hasFixtureMissing|'
      'platform=${selectedPlatformKind()}|mode=$deploymentMode';
}
