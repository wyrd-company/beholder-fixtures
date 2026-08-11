// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

// Side-effect import that installs the runtime patch (TS-CAN-021)
import "./side-effect-patch.js";

export function describePatch(): boolean {
  return globalThis.harborPatchApplied === true;
}
