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

/// StorageCrate's name parts, generated with a source trailing comma
/// (DART-CAN-BUILD-004 formatter-style contrast). This library formats
/// under this generator's explicit `@dart=3.6` header override, under which
/// `dart format` treats a source trailing comma as a signal to keep a
/// same-line-eligible list split across lines, so this list stays split.
/// Compare `tool_record.g.dart`'s identically-shaped `_torqueWrenchNameParts`,
/// generated at the package's current default language version, where the
/// same trailing comma does not prevent the list from collapsing onto one
/// line.
const List<String> _storageCrateNameParts = [
  'storage',
  'crate',
];

/// Joins _storageCrateNameParts, so the formatter-style contrast list above is
/// generated content actually reachable from StorageCrate, not dead code.
String describeStorageCrateNameParts() => _storageCrateNameParts.join(' ');
