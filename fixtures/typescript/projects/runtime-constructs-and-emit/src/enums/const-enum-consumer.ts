// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

import { ExportedConst } from "./const-enum.js";

export function consumeCrossBoundaryConst(value: ExportedConst): string {
  return `cross:${value}:${ExportedConst.Green}`;
}

export function crossBoundaryInlinedValue(): number {
  return ExportedConst.Red;
}
