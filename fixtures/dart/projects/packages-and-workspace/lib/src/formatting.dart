/// Renders a console report line from a greeting, a ledger summary, and the
/// raw command-line arguments the entry point received.
String formatReport(
  String greeting,
  String ledgerSummary,
  List<String> arguments,
) {
  final argSuffix = arguments.isEmpty ? 'no arguments' : arguments.join(', ');
  return '$greeting | $ledgerSummary | args: $argSuffix';
}
