import 'package:ledger_support/ledger_support.dart';

import 'data_lookup.dart';
import 'formatting.dart';

/// Root application logic, composing the `ledger_support` workspace member
/// with this package's own data lookup and formatting.
class ConsoleApp {
  final Ledger _ledger = Ledger();

  Future<String> report(List<String> arguments) async {
    for (final argument in arguments) {
      final value = double.tryParse(argument);
      if (value != null) {
        _ledger.record('console', value);
      }
    }
    final greeting = await loadGreeting();
    return formatReport(greeting, _ledger.describe(), arguments);
  }
}
