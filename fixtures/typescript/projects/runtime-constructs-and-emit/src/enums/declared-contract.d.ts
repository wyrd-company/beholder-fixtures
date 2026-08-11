// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

// Declaration-only contract for a companion runtime module. The program never
// contains the implementing `declared-contract.js`; it consumes only this
// hand-authored declaration. That makes the boundary a real declaration
// boundary rather than a same-program source-module boundary: a `const enum`
// reached through it is inlined and its import is elided, while an ordinary
// enum reached through it keeps a runtime module reference in emitted output.

export const enum DeclaredConst {
  North = 0,
  East = 1,
  South = 2,
  West = 3,
}

export enum DeclaredOrdinary {
  Spring = 1,
  Summer = 2,
  Autumn = 3,
  Winter = 4,
}
