// ---
// relationships:
//   implements: esm-cjs-interop
//   references: ground-rules
// ---

/// <reference path="../types/dial.d.ts" />

declare const Dial: typeof import("../types/dial.js");

function readDialFromScript(): number {
  return Dial.spin();
}

readDialFromScript();
