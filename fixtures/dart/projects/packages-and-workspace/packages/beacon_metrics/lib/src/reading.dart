import 'package:clock/clock.dart';

/// A single beacon measurement, stamped with the ambient [Clock].
class BeaconReading {
  const BeaconReading({
    required this.stationId,
    required this.value,
    required this.observedAt,
  });

  final String stationId;
  final double value;
  final DateTime observedAt;

  @override
  String toString() => 'BeaconReading($stationId, $value, $observedAt)';
}

/// Takes a reading for [stationId], stamping it with the package:clock
/// hosted-source dependency (substituted with a local path fork by the
/// workspace root's override; see ../../../pubspec_overrides.yaml).
BeaconReading takeReading(String stationId, double value) {
  return BeaconReading(
    stationId: stationId,
    value: value,
    observedAt: clock.now(),
  );
}
