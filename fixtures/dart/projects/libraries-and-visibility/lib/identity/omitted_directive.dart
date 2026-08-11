// This file has no library directive at all. It is still its own namespace
// and privacy unit: the omitted form is exactly equivalent to `library;` for
// resolution and privacy purposes.

class OmittedDirectiveMarker {
  const OmittedDirectiveMarker();
}

String omittedDirectiveLabel() => 'omitted';
