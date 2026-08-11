// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

/// <reference path="./lib-stub.d.ts" />

interface LibStubClock {
  tick(): number;
}

declare const LibStubClock: LibStubClock;
