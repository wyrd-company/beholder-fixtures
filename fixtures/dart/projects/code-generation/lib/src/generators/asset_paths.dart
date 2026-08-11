import 'package:build/build.dart';

/// `AssetId.changeExtension` strips only the last dot-segment, which mangles
/// a compound suffix such as `.catalog.json`; replace the whole suffix by
/// hand so the catalog builder chain can produce assets with multi-part
/// extensions.
AssetId withSuffix(AssetId input, String oldSuffix, String newSuffix) {
  final path = input.path;
  return AssetId(
    input.package,
    '${path.substring(0, path.length - oldSuffix.length)}$newSuffix',
  );
}
