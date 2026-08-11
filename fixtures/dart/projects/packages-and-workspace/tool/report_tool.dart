import 'dart:io';

/// `tool/` root entry library. Unlike `lib/src/data_lookup.dart`, which
/// resolves its data file by `package:` URI through the generated package
/// configuration, this script looks up `notes.txt` by a path relative to
/// its own script location — a root-local lookup with no `package:` URI,
/// since `tool/` files are not addressable through one
/// (DART-CAN-PKG-002's "different reachability per root").
void main() {
  final notesUri = Platform.script.resolve('notes.txt');
  stdout.writeln(File.fromUri(notesUri).readAsStringSync().trim());
}
