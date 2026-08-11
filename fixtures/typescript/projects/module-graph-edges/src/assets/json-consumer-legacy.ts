// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

// Legacy assertion contrast (TS-CAN-023) — `assert` syntax predates `with`.
// Modern: `with { type: "json" }`; legacy: `assert { type: "json" }` (TS 5.9 uses `with`).
import harborLegacy from "./data.json" with { type: "json" };

export function describeLegacyJson(): string {
  return harborLegacy.harbor;
}
