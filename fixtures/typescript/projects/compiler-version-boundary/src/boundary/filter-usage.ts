// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

// Demonstrates the observable consequence of the inferred predicate boundary
// when the predicate is used with Array.prototype.filter. Under 5.4.5 the
// predicate remains boolean, so filter does not narrow; under 5.9.3 it does.

import { isString } from "./predicate.js";

export function getStrings(values: unknown[]) {
  return values.filter(isString);
}

export function countStrings(values: unknown[]): number {
  return getStrings(values).length;
}
