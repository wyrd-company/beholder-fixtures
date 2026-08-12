// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

// Unused deferred binding (TS-CAN-033) — imported but never accessed
import defer * as UnusedNs from "./side-effectful.js";

export function describeUnused(): string {
  return "unused-defer-present";
}

// The deferred import itself retains the module-graph edge; no member access
// is required and none is performed, satisfying the "unused" variant.
