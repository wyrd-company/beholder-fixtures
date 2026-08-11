library;

// An alternate native branch used only to demonstrate first-match
// conditional-import selection in `first_match_selector.dart`: it is never
// actually selected there because `platform_native.dart` matches first.
import 'dart:io';

String platformLabel() => 'native-alt:${Platform.operatingSystem}';
