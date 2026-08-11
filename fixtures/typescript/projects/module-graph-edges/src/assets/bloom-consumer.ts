// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

// Custom extension typed through wildcard and per-file declarations (TS-CAN-023)
// Requires allowArbitraryExtensions.
import bloomContent from "./note.bloom";

export function describeBloom(): string {
  return bloomContent;
}
