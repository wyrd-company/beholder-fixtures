import 'package:beacon_metrics/beacon_metrics.dart';
import 'package:ledger_support/ledger_support.dart';
import 'package:test/test.dart';

import 'support/reading_matchers.dart';

/// Exercises the workspace members directly (DART-CAN-PKG-006) by
/// `package:` URI, importing the same shared resolution `bin/` and `lib/`
/// use.
void main() {
  group('beacon_metrics readings', () {
    test('take a reading stamped for the given station', () {
      final reading = takeReading('north-dock', 12.5);
      expect(reading, isReadingFor('north-dock'));
      expect(reading.value, 12.5);
    });
  });

  group('ledger_support channel and ledger', () {
    late Ledger ledger;

    setUp(() => ledger = Ledger());

    test('describes zero entries before any record', () {
      expect(ledger.describe(), contains('0 entries'));
    });

    test('accumulates entries across records', () async {
      ledger.record('south-dock', 1);
      ledger.record('south-dock', 2);
      await Future<void>.delayed(Duration.zero);
      expect(ledger.entries, hasLength(2));
      expect(ledger.describe(), contains('2 entries'));
    });
  }, tags: ['smoke']);
}
