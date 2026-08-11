// ---
// relationships:
//   implements: esm-cjs-interop
//   references: ground-rules
// ---

/// <reference path="../types/dial.d.ts" />

declare const Dial: typeof import("../types/dial.js");

export function readDialGlobal(): number {
  return Dial.spin();
}
