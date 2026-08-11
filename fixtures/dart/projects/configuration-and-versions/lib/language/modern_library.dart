/// Modern library at the package default language version.
library;

/// Record syntax introduced in Dart 3.
typedef Coordinate = (int x, int y);

/// Returns the fixture origin using a post-3.0 feature.
Coordinate originCoordinate() => (0, 0);
