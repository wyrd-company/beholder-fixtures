// ---
// relationships:
//   implements: esm-cjs-interop
//   references: ground-rules
// ---

function localA(): string {
  return localB();
}

function localB(): string {
  return "hoisted";
}

import { triggerB } from "./hoist-b.js";

export function entryA(): string {
  return triggerB();
}
