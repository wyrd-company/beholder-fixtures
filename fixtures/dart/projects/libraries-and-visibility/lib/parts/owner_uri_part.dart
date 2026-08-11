part of 'owner_uri.dart';

// Reads the owning library's private top-level variable directly: parts
// share their owning library's namespace and private names.
int readOwnerUriCounterFromPart() => _ownerUriPrivateCounter;

// Resolves `pi`, brought into scope only by the owning library's own
// `import 'dart:math' show pi;`: this part declares no import of its own
// and shares the owning library's import scope, not just its namespace and
// private names.
double readImportedPiFromPart() => pi;
