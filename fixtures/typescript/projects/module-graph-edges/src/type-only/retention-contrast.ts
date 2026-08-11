// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

// Same unmarked import under legacy elision and verbatimModuleSyntax:
// HarborBuoy is used only as a type here. Under legacy elision the import
// is removed; under verbatimModuleSyntax it is retained.

import { HarborBuoy } from "./models.js";

export type HarborBuoyType = HarborBuoy;

export function createBuoy(beacon: number): HarborBuoyType {
  // Type-only usage; value constructor not needed because type position
  return { beacon, ping: () => `ping:${beacon}` } as HarborBuoy;
}

// Inline type modifier contrast (TS-CAN-019)
import { type TideLevel } from "./models.js";

export type TideLevelAliasLocal = TideLevel;
