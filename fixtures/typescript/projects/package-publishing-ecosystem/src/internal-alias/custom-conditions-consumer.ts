// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

import { read, marker } from "@fixtures/custom-conditions-dep";
import type { CustomDepDefault } from "@fixtures/custom-conditions-dep";

export function describeCustomConditions(value: string): string {
  const a = read(value);
  return `${a}|${marker}`;
}

export type CustomSurface = CustomDepDefault;

// Import/require branches are demonstrated by the dependency's export map having
// separate import/require entries for the same specifier; this consumer uses the import branch.
