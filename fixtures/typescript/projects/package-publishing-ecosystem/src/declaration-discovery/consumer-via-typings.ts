// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

import { readViaTypings } from "@fixtures/typed-via-typings";
import type { ViaTypingsMarker } from "@fixtures/typed-via-typings";

export function describeViaTypings(value: string): string {
  return readViaTypings(value);
}

export type TypingsMarker = ViaTypingsMarker;
