// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

import type { HostFlipSentinel } from "./host-flip-sentinel.js";

declare global {
  declare var ModuleScopedHostCounter: number;

  interface ModuleFlipMarker {
    sentinel: HostFlipSentinel;
  }
}

export {};
