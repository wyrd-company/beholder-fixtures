// ---
// relationships:
//   implements: esm-cjs-interop
//   references: ground-rules
// ---

function localB(): string {
  return localA();
}

function localA(): string {
  return "hoisted";
}

import { entryA } from "./hoist-a.js";

export function triggerB(): string {
  return entryA();
}
