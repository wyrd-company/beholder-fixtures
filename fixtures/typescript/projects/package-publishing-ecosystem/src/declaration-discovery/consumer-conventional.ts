// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

import { readConventional } from "@fixtures/typed-conventional";
import type { ConventionalMarker } from "@fixtures/typed-conventional";

export function describeConventional(value: string): string {
  return readConventional(value);
}

export type ConvMarker = ConventionalMarker;
