import '../annotations.dart';

/// A pinned, annotation-triggered builder (`crateManifestBuilder`,
/// registered in `build.yaml`) emits `crate_manifest.crate.g.dart`, a
/// standalone generated library — distinct from a `part` output, with no
/// `part` directive here.
@CrateManifest()
class StorageCrate {
  const StorageCrate(this.crateId, this.capacity);

  final String crateId;
  final int capacity;
}
