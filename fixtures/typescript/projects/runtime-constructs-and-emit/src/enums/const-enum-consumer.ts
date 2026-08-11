// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

import { DeclaredConst, DeclaredOrdinary } from "./declared-contract.js";

// `DeclaredConst` is reached only through the declaration contract. Across that
// declaration boundary the compiler inlines each member as a literal and emits
// no import edge to `./declared-contract.js` for it.
export function consumeCrossBoundaryConst(): string {
  return `cross:${DeclaredConst.East}:${DeclaredConst.West}`;
}

export function crossBoundaryInlinedValue(): number {
  return DeclaredConst.North;
}

// `DeclaredOrdinary` is reached through the same declaration boundary, but an
// ordinary enum has runtime identity: the emit keeps a runtime module reference
// to `./declared-contract.js` plus property and reverse-map access.
export function consumeCrossBoundaryOrdinary(): string {
  return `ordinary:${DeclaredOrdinary.Summer}:${DeclaredOrdinary[DeclaredOrdinary.Summer]}`;
}
