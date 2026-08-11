// ---
// relationships:
//   implements: esm-cjs-interop
//   references: ground-rules
// ---

import measureSpan from "../../deps/callable-cjs/index.js";

export function nativeSpan(left: number, right: number): number {
  return measureSpan(left, right);
}
