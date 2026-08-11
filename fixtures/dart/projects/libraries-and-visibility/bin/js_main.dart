import 'package:libraries_and_visibility/conditional/platform_api.dart'
    as platformApi;
import 'package:libraries_and_visibility/conditional/platform_selector.dart';
import 'package:libraries_and_visibility/deferred/deferred_payload.dart'
    deferred as payload;

Future<void> main() async {
  print(platformApi.platformLabel());
  print(describePlatform());

  await payload.loadLibrary(); // Web code-splitting load unit.
  await payload.loadLibrary(); // Repeated loadLibrary().
  for (final value in payload.payloadValues) {
    print(payload.describePayload(value));
  }
}
