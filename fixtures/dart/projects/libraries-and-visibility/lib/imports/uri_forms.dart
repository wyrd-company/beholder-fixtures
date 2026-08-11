library;

import 'dart:math' show pi; // `dart:` URI authority.
import 'package:libraries_and_visibility/identity/omitted_directive.dart'; // `package:` URI authority.
import '../identity/unnamed_directive.dart'; // Relative URI authority.

// No explicit `dart:core` import appears in this file: `List` and `String`
// below resolve through the implicit `dart:core` import every library
// receives.
List<String> describeUriForms() => <String>[
  'pi=$pi',
  omittedDirectiveLabel(),
  unnamedDirectiveLabel(),
];
