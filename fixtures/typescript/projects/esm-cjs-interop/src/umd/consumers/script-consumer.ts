// ---
// relationships:
//   implements: esm-cjs-interop
//   references: ground-rules
// ---

/// <reference path="../types/dial.d.ts" />

function readDialFromScript(): number {
  return Dial.spin();
}

readDialFromScript();
