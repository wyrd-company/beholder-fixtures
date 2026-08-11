// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

import { describeSelf } from "self-ref-pkg";

export function describeSelfImport(value: string): string {
  return describeSelf(value);
}
