// ---
// relationships:
//   implements: esm-cjs-interop
//   references: ground-rules
// ---

import { tokenA } from "./barrel-a.js";

export function readTokenB(): string {
  return tokenA;
}
