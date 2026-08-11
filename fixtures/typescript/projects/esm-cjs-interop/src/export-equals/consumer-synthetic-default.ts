// ---
// relationships:
//   implements: esm-cjs-interop
//   references: ground-rules
// ---

import Chronometer from "./chronometer.cjs.js";

export function readSyntheticDefaultUnit(): string {
  return Chronometer.unit;
}
