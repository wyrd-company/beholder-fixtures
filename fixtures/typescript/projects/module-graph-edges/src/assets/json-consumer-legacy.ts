// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

// Legacy assertion contrast (TS-CAN-023) — historical `assert` syntax predates `with`.
// Bob determination 2026-08-12: do not support `assert { type: "json" }`; it is
// historical/unsupported on TypeScript 5.9.3 (TS2880). Valid coverage uses
// `with { type: "json" }`. The old form `import data from "./data.json"
// assert { type: "json" }` is documented here only as a counterexample.
import harborLegacy from "./data.json" with { type: "json" };

export function describeLegacyJson(): string {
  return harborLegacy.harbor;
}
