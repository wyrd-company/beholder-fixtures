/// A const value declared in one library so that
/// [DART-CAN-CONST-002]'s cross-library canonicalization can compare it
/// against an equal const value declared in another library.
library;

import 'basics.dart';

const Money originMoney = Money(0);
