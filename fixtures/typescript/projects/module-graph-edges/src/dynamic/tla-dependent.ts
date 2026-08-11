// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

import { awaitedTide } from "./tla-entry.js";

export function describeDependent(): string {
  return `dependent:${awaitedTide}`;
}
