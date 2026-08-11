// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

// Consumes the vendored dependency that declares a minimum compiler version
// (peerDependencies: typescript >=5.5). The dependency exists to make the
// version requirement observable as part of program identity. The cast keeps
// the consumer valid under both 5.4.5 (boolean) and 5.9.3 (predicate).

import {
  wrapGuard,
  type PredicateGuard,
} from "@fixtures/requires-predicate-inference";
import { isString } from "./boundary/predicate.js";

export const guardedIsString: PredicateGuard<string> = wrapGuard(
  isString as PredicateGuard<string>,
);

export function filterWithGuard(values: unknown[]): string[] {
  return values.filter(guardedIsString);
}
