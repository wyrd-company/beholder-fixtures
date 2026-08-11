// ---
// relationships:
//   implements: esm-cjs-interop
//   references: ground-rules
// ---

import { mutableCount } from "./esm-a.js";

export function readMutableFromB(): number {
  return mutableCount;
}
