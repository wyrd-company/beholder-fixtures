import 'package:beacon_metrics/beacon_metrics.dart';
import 'package:test/test.dart';

/// A test-only helper library: reachable only from within the `test/` root
/// (imported by relative path from sibling test files), never from `lib/`,
/// `bin/`, `example/`, or `tool/` (DART-CAN-PKG-002's test-root
/// reachability).
Matcher isReadingFor(String stationId) {
  return isA<BeaconReading>().having(
    (reading) => reading.stationId,
    'stationId',
    stationId,
  );
}
