/// The second of two libraries that share a documentary (legacy) library
/// name with `legacy_named_alpha.dart`. Declares a distinctly named export
/// so importing both alongside each other never collides.
library fixture.identity.shared;

String sharedNameOtherLabel() => 'beta';
