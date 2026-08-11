library;

// The conditional-import counterpart to `platform_api.dart`'s conditional
// export: same common API, selected the same way.
import 'platform_default.dart'
    if (dart.library.io) 'platform_native.dart'
    if (dart.library.js_interop) 'platform_web.dart'
    as impl;

String describePlatform() => impl.platformLabel();
