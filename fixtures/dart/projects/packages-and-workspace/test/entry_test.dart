import 'package:signal_console/signal_console.dart';
import 'package:test/test.dart';

/// `test/` root entry library (DART-CAN-PKG-002, DART-CAN-PKG-007): imports
/// the fixture-owned package by `package:` URI, exactly as an external
/// consumer would, and is reachable only from within the `test/` root — no
/// `lib/`, `bin/`, `example/`, or `tool/` source imports it back.
///
/// It uses only `signal_console`'s exported façade (`ConsoleApp`,
/// `formatReport`); `lib/src/*.dart`'s private (`_`-prefixed) members stay
/// out of reach here because each `.dart` file is its own library, and
/// Dart's privacy boundary is per-library, not per-directory — the valid
/// side of that boundary, demonstrated by not needing any private access.
void main() {
  group('ConsoleApp reporting', () {
    late ConsoleApp app;

    setUp(() {
      app = ConsoleApp();
    });

    tearDown(() {
      // No teardown state to release; present to demonstrate the lifecycle
      // hook alongside setUp.
    });

    test('formats a report synchronously from readable arguments', () {
      final formatted = formatReport('hi', 'ledger: 0 entries', const [
        'a',
        'b',
      ]);
      expect(formatted, 'hi | ledger: 0 entries | args: a, b');
    });

    test(
      'reports asynchronously and records numeric arguments',
      () async {
        final report = await app.report(const ['1.5', 'ignored', '2.5']);
        expect(report, contains('2 entries'));
        expect(report, contains('args: 1.5, ignored, 2.5'));
      },
      testOn: 'vm',
      tags: ['smoke'],
    );

    test(
      'handles a large synthetic argument batch',
      () async {
        final many = List.generate(50, (i) => '$i');
        final report = await app.report(many);
        expect(report, contains('50 entries'));
      },
      tags: ['slow'],
      timeout: const Timeout(Duration(seconds: 5)),
    );

    test(
      'is skipped pending a future console backend',
      () {
        fail('not reached: skipped');
      },
      skip: 'placeholder for a future console backend variant',
    );
  });
}
