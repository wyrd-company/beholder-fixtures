// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

// Ordinary namespace import of side-effectful module — evaluates immediately
import * as EagerNs from "./side-effectful.js";

export function describeEager(): string {
  return EagerNs.sideEffectTag;
}

export function readEagerCounter(): number {
  return EagerNs.harborTideCounter.count;
}
