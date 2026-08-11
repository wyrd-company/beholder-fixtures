library;

import 'legacy_named_alpha.dart';
import 'legacy_named_beta.dart';

// Both libraries declare `library fixture.identity.shared;`. Import
// resolution is by URI, not by this documentary name, so both are usable
// side by side with no name collision at the import level.
String describeIdentitySources() =>
    '${sharedNameLabel()}/${sharedNameOtherLabel()}';
