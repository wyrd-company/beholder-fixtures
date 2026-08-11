/// Applied-fix counterpart for DART-CAN-DIAG-007.
///
/// This file shows the state after the automated fix has been applied.
/// The deprecated call has been rewritten to the current API.
library;

import 'package:helper/helper.dart';

String useMigrated() => helperNew('d-1');
