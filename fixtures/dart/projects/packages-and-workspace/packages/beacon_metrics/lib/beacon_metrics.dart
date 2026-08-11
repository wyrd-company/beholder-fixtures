/// Public façade for the `beacon_metrics` workspace member.
///
/// Re-exports the implementation library under `src/`, so importers see one
/// stable `package:beacon_metrics/beacon_metrics.dart` surface.
library;

export 'src/reading.dart' show BeaconReading, takeReading;
