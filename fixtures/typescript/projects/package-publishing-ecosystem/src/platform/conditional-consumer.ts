// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

import { getPlatform } from "./entry.js";
import { getEnv } from "./feature.js";
import type { PlatformMarker } from "./entry.js";

export function describeConditional(): string {
  return `${getPlatform()}:${getEnv()}`;
}

export type CondensedMarker = PlatformMarker;

// Condition-selected browser/server/native via @fixtures/platform-pkg import condition.
// Suffix-selected via moduleSuffixes on ./entry (entry.browser.ts etc) is observable in dist-platform emit.
