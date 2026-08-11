// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

import type { HostFlipSentinel } from "./host-flip-sentinel.js";

export function readModuleScopedHostCounter(): number {
  return ModuleScopedHostCounter;
}

export function readModuleFlipMarker(): ModuleFlipMarker {
  return { sentinel: "module-flipped" as HostFlipSentinel };
}

declare global {
  interface ModuleHostMarker {
    scope: "module-global-augment";
  }
}

export function readModuleHostMarker(): ModuleHostMarker {
  return { scope: "module-global-augment" };
}
