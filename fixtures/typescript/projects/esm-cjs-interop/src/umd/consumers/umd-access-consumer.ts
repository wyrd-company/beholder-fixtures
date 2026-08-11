// ---
// relationships:
//   implements: esm-cjs-interop
//   references: ground-rules
// ---

/// <reference path="../types/dial.d.ts" />

export function readDialGlobal(): number {
  return Dial.spin();
}
