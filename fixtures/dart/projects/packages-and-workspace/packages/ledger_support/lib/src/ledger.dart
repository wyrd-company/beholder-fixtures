import 'package:beacon_metrics/beacon_metrics.dart';

import 'channel.dart';

/// Records [BeaconReading]s taken through the `beacon_metrics` sibling
/// member, reached by a cross-member `package:` import (DART-CAN-PKG-006).
class Ledger {
  final List<BeaconReading> _entries = [];

  void record(String stationId, double value) {
    _entries.add(takeReading(stationId, value));
  }

  List<BeaconReading> get entries => List.unmodifiable(_entries);

  String describe() => '${describeChannel()}: ${_entries.length} entries';
}
