/// Conditional import that pairs environment values with platform libraries.
library;

export 'package:configuration_and_versions/environment/platform_stub.dart'
    if (dart.library.io) 'package:configuration_and_versions/environment/platform_io.dart'
    if (dart.library.js) 'package:configuration_and_versions/environment/platform_js.dart';
