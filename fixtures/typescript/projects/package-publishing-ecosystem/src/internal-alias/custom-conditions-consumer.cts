// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

import { read } from "@fixtures/custom-conditions-dep";
import type { CustomDepDefault } from "@fixtures/custom-conditions-dep";

export function describeCustomConditionsRequire(value: string): string {
  return read(value);
}

export type RequireSurface = CustomDepDefault;
