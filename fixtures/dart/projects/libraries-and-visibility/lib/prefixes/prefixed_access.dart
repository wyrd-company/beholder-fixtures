library;

import 'dart:math'; // Unprefixed import.
import 'dart:math'
    as mathPrefixed; // Repeated import of one library, this time prefixed.
import 'dart:convert' as shared; // Multiple imports sharing one prefix...
import 'dart:math'
    as shared; // ...continued: `shared` merges `dart:convert` and `dart:math`.
import 'describable_extension.dart'
    as ext; // Explicit extension application through a prefix.
import '../deferred/deferred_payload.dart'
    deferred as payloadPrefix; // A deferred import needs its own, non-shared prefix.

String describePrefixedAccess() {
  final unprefixedArea =
      pi * 2; // Unprefixed `pi` from the plain `dart:math` import.
  final prefixedSqrt = mathPrefixed.sqrt(16);
  final mergedJsonAndMax = shared.jsonEncode(<String, int>{
    'k': shared.max(1, 2),
  });
  final extensionResult = ext.DescribableExtension(3).describe();
  return '$unprefixedArea/$prefixedSqrt/$mergedJsonAndMax/$extensionResult';
}

Future<int> loadDeferredPayloadCountViaDistinctPrefix() async {
  await payloadPrefix.loadLibrary();
  return payloadPrefix.payloadValues.length;
}
