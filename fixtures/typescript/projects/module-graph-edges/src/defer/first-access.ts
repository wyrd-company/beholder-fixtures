// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

import defer * as DeferredHarbor from "./side-effectful.js";

export function firstMemberAccess(): string {
  // Explicit first member access observable point
  const tag = DeferredHarbor.sideEffectTag;
  const count = DeferredHarbor.harborTideCounter.count;
  return `${tag}:${count}`;
}
