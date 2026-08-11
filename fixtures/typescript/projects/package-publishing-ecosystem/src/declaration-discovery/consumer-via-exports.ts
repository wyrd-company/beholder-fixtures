// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

import { readViaExports } from "@fixtures/typed-via-exports";
import type { ViaExportsMarker } from "@fixtures/typed-via-exports";

export function describeViaExports(value: string): string {
  return readViaExports(value);
}

export type ExportsMarker = ViaExportsMarker;
