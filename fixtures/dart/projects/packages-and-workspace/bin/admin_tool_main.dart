import 'dart:io';

import 'package:beacon_metrics/beacon_metrics.dart';
import 'package:ledger_support/ledger_support.dart';

/// Second named executable (`admin-tool`), demonstrating a second `bin/`
/// entry point (DART-CAN-PKG-002) that imports workspace members directly
/// rather than through the root façade, and that is invoked with a
/// different argument shape than `console_main.dart`
/// (DART-CAN-PKG-008: `dart run bin/admin_tool_main.dart -- <station> <value>...`).
void main(List<String> arguments) {
  if (arguments.length < 2) {
    stderr.writeln('usage: admin-tool <station-id> <value> [value...]');
    exitCode = 64;
    return;
  }
  final stationId = arguments.first;
  final ledger = Ledger();
  for (final raw in arguments.skip(1)) {
    final value = double.tryParse(raw);
    if (value != null) {
      final reading = takeReading(stationId, value);
      ledger.record(stationId, value);
      stdout.writeln('recorded $reading');
    }
  }
  stdout.writeln(ledger.describe());
}
