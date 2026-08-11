// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

// Deferred namespace import — evaluation deferred until first member access (TS-CAN-033)
import defer * as DeferNs from "./side-effectful.js";

export function describeDeferFirstAccess(): string {
  // First member access triggers evaluation
  return DeferNs.sideEffectTag;
}

export function readDeferCounter(): number {
  return DeferNs.harborTideCounter.count;
}
