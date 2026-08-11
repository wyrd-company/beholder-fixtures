// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

import { readMismatch } from "@fixtures/mismatch-pkg";
import type { MismatchMarker } from "@fixtures/mismatch-pkg";

// Type-checks against declarations, but runtime entry exports readOther instead of readMismatch.
// This mismatch is intentionally valid source — loader would fail, but tsc succeeds.

export function describeMismatch(value: string): string {
  return readMismatch(value);
}

export type ConsumerMismatch = MismatchMarker;
