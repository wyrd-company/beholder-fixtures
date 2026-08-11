// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

import { legacyRead } from "@fixtures/legacy-fallback";
import type { MainBeacon } from "@fixtures/exports-map";

export function describeLegacy(value: string): string {
  return legacyRead(value);
}

export function mapLegacyToBeacon(value: string): MainBeacon {
  return { id: legacyRead(value) };
}
