import 'package:build/build.dart';
import 'package:source_gen/source_gen.dart';

import 'generators/catalog_data_builder.dart';
import 'generators/catalog_index_builder.dart';
import 'generators/crate_manifest_generator.dart';
import 'generators/tool_summary_generator.dart';

const _generatedHeader = '''
// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint''';

/// [crateManifestBuilder]'s output pins an older per-library language
/// version (DART-CAN-BUILD-004): `tool_record.g.dart` formats under the
/// package's current, default language version (the "tall" style), while
/// this standalone library formats under an explicit `3.6` override (the
/// pre-3.7 style) — two formatter styles, coexisting validly, with no
/// semantic difference in either generated library's content.
const _crateManifestHeader = '''
// GENERATED CODE - DO NOT MODIFY BY HAND
// @dart=3.6
// ignore_for_file: type=lint''';

/// Builder factory named by `build.yaml`'s `tool_summary_builder` definition
/// (DART-CAN-BUILD-001): emits the `.g.dart` part driven by the
/// `ToolSummary` annotation.
Builder toolSummaryBuilder(BuilderOptions options) => PartBuilder(
  [const ToolSummaryGenerator()],
  '.g.dart',
  header: _generatedHeader,
);

/// Builder factory named by `build.yaml`'s `crate_manifest_builder`
/// definition (DART-CAN-BUILD-002): emits a standalone generated library
/// driven by the `CrateManifest` annotation.
Builder crateManifestBuilder(BuilderOptions options) => LibraryBuilder(
  const CrateManifestGenerator(),
  generatedExtension: '.crate.g.dart',
  header: _crateManifestHeader,
);

/// Builder factory named by `build.yaml`'s `catalog_index_builder`
/// definition (DART-CAN-BUILD-003, first stage): normalizes the non-Dart
/// `.catalog.json` input into a hidden, cache-only intermediate asset
/// consumed by `catalogDataBuilder`.
Builder catalogIndexBuilder(BuilderOptions options) =>
    const CatalogIndexBuilder();

/// Builder factory named by `build.yaml`'s `catalog_data_builder` definition
/// (DART-CAN-BUILD-003, second stage): a transitive builder that reads
/// `catalogIndexBuilder`'s output, not the original `.catalog.json` source,
/// and emits the committed `.catalog.g.dart` library. The `include_codes`
/// option is read from `build.yaml`'s `options:` block.
Builder catalogDataBuilder(BuilderOptions options) => CatalogDataBuilder(
  includeCodes: options.config['include_codes'] as bool? ?? true,
);
