/// A library owning a classic part, addressed by URI `part of`. The part
/// shares this library's imports, namespace, and private names.
library;

import 'dart:math' show pi;

part 'owner_uri_part.dart';

int _ownerUriPrivateCounter = 0;

void bumpOwnerUriCounter() {
  _ownerUriPrivateCounter++;
}
