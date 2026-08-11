---
relationships:
  references:
    - ground-rules
    - configuration-and-versions
    - reports/dart/synthesis/checklist
---

# Configuration and versions coverage

| Canonical checklist identifier | Stable source path | Named declaration, directive, library, package, or test | Build context | Additional variant locators |
| --- | --- | --- | --- | --- |
| DART-CAN-CFG-001 | `pubspec.yaml`, `lib/sdk_pin.dart`, `lib/language/modern_library.dart`, `lib/language/legacy_consumer.dart` | `environment.sdk` lower bound `>=3.12.2 <4.0.0`; `pinnedSdkLowerBound`; `selectedSdkVersion`; `Coordinate`; `originCoordinate`; `Pair`; `pairFromOrigin` | Default (`vm-jit`) | `legacy_consumer.dart` uses `// @dart=2.19` while `modern_library.dart` keeps the package default and records syntax; importing `modern_library.dart` keeps the dependency at its own resolved version |
| DART-CAN-CFG-002 | `lib/language/versioned_library.dart`, `lib/language/versioned_library_part.dart`, `lib/language/pre_super_params.dart`, `lib/language/post_super_params.dart` | `versioned_library_part.dart` inherits the owning library package-default version; `CounterHolder`; `bumpCounter`; `// @dart=2.16` on `pre_super_params.dart`; `// @dart=2.17` on `post_super_params.dart`; `ForwardedValue`; `SuperForwardedSlot` | Default (`vm-jit`) | `pre_super_params.dart` is pre-super-parameter forwarding; `post_super_params.dart` is post-super-parameter forwarding |
| DART-CAN-CFG-003 | `lib/environment/compile_time.dart`, `lib/environment/platform_selector.dart`, `lib/environment/platform_stub.dart`, `lib/environment/platform_io.dart`, `lib/environment/platform_js.dart`, `bin/js_main.dart` | `fixtureString`; `fixtureInt`; `fixtureBool`; `hasFixtureString`; `hasFixtureMissing`; `deploymentMode`; `environmentSummary`; conditional import in `platform_selector.dart`; `selectedPlatformKind` | `js` for analyzer-default versus compiled `fixtureString` in `js_main.dart`; default (`vm-jit`) for the remaining environment constants | `Taskfile.yml` supplies `-DFIXTURE_STRING=alpha`, `-DFIXTURE_INT=3`, `-DFIXTURE_BOOL=true`, and `-DDEPLOY_MODE=compiled`; `js` build adds `-DFIXTURE_STRING=compiled-value`; defaults remain `analyzer-default`, `7`, `false`, and `local` |
| DART-CAN-CFG-004 | `lib/assertions/checks.dart`, `bin/vm_main.dart`, `bin/native_aot_main.dart`, `Taskfile.yml` | `assertionCondition`; `runAssertionProbe`; `assert(..., 'fixture assertion message')`; `--expect-asserts` in `vm_main.dart` | `vm-jit` for development-default and disabled assertion runs; `native-aot` for production-default and explicitly enabled assertion compilation | `build` runs `dart run` without an assertion-mode flag and `dart run --no-enable-asserts`; `dart compile exe` without asserts and with `--enable-asserts`; disabled assertions skip `assertionSideEffectCount` increments |
