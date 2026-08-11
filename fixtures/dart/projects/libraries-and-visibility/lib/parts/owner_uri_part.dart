part of 'owner_uri.dart';

// Reads the owning library's private top-level variable directly: parts
// share their owning library's namespace and private names.
int readOwnerUriCounterFromPart() => _ownerUriPrivateCounter;
