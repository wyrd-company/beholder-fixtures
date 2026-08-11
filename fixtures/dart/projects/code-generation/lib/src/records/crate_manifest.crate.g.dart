// GENERATED CODE - DO NOT MODIFY BY HAND
// dart format width=80

// @dart=3.6
// ignore_for_file: type=lint

// **************************************************************************
// CrateManifestGenerator
// **************************************************************************

import 'package:toolshed_catalog/src/records/crate_manifest.dart';

/// Private to this generated library: not reachable from
/// `lib/src/records/crate_manifest.dart` or any other file, even though that file
/// declares [StorageCrate] and this function's own annotation is read from it.
String _storageCrateLabel(StorageCrate crate) => 'crate-${crate.crateId}';

/// Public façade over the generated crate description, reachable by any
/// importer of this standalone generated library.
String describeStorageCrate(StorageCrate crate) =>
    '${_storageCrateLabel(crate)} (capacity ${crate.capacity})';
