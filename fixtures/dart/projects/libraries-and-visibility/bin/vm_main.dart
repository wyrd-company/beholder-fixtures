import 'package:libraries_and_visibility/conditional/platform_api.dart'
    as platformApi;
import 'package:libraries_and_visibility/conditional/platform_selector.dart';
import 'package:libraries_and_visibility/conditional/first_match_selector.dart';
import 'package:libraries_and_visibility/deferred/deferred_payload.dart'
    deferred as payload;

Future<void> main() async {
  print(platformApi.platformLabel());
  print(describePlatform());
  print(describeFirstMatchSelection());

  await payload.loadLibrary(); // VM trivial load.
  await payload
      .loadLibrary(); // Repeated loadLibrary() on an already-loaded deferred library.
  for (final value in payload.payloadValues) {
    print(payload.describePayload(value));
  }
}
