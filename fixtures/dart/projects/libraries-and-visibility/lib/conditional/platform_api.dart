library;

// A conditional export behind one common API (`platformLabel()`): the
// default branch is unconditional, and each `if` branch is selected by a
// `dart.library.*` environment condition at compile/analysis time.
//
// The Dart analyzer resolves this file's own static analysis using the
// default (unconditional) branch, `platform_default.dart`, regardless of
// build context; only compilation (`dart run`/`dart compile`) selects the
// declared-environment branch.
export 'platform_default.dart'
    if (dart.library.io) 'platform_native.dart'
    if (dart.library.js_interop) 'platform_web.dart';
