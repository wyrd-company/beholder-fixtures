/// Assertion configuration demonstrations for [DART-CAN-CFG-004].
library;

/// Counts how many times an assertion condition evaluated.
int assertionSideEffectCount = 0;

/// Side effect observed only when assertions execute.
bool assertionCondition() {
  assertionSideEffectCount++;
  return true;
}

/// Runs an assertion with a message and reports whether it executed.
bool runAssertionProbe() {
  assertionSideEffectCount = 0;
  assert(assertionCondition(), 'fixture assertion message');
  return assertionSideEffectCount > 0;
}
