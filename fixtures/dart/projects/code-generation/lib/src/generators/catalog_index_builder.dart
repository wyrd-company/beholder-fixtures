import 'dart:convert';

import 'package:build/build.dart';

import 'asset_paths.dart';

/// First stage of the two-stage catalog builder chain (DART-CAN-BUILD-003).
///
/// Reads the non-Dart `.catalog.json` input, sorts its `tools` list by
/// `code` for a deterministic order, and writes a `.catalog.index.json`
/// asset. `build.yaml` configures this builder with `build_to: cache`, so
/// the normalized index never lands in `lib/` or gets committed; it exists
/// only to feed [CatalogDataBuilder], the transitive builder that consumes
/// it instead of the original source.
class CatalogIndexBuilder implements Builder {
  const CatalogIndexBuilder();

  @override
  Map<String, List<String>> get buildExtensions => const {
    '.catalog.json': ['.catalog.index.json'],
  };

  @override
  Future<void> build(BuildStep buildStep) async {
    final input = buildStep.inputId;
    final source =
        jsonDecode(await buildStep.readAsString(input)) as Map<String, dynamic>;

    final tools =
        (source['tools'] as List<dynamic>).cast<Map<String, dynamic>>().toList()
          ..sort(
            (a, b) => (a['code'] as String).compareTo(b['code'] as String),
          );

    final index = <String, dynamic>{
      'crateId': source['crateId'],
      'tools': tools,
    };

    final output = withSuffix(input, '.catalog.json', '.catalog.index.json');
    await buildStep.writeAsString(
      output,
      const JsonEncoder.withIndent('  ').convert(index),
    );
  }
}
