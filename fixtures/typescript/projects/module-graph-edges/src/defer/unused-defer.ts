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

// Keep binding alive for graph but not accessed — the existence of the
// import defer itself is the corpus content, not its usage.
void UnusedNs;
