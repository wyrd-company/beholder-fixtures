// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

import { internalMarker } from "#internal/index.js";
import { extraMarker } from "#internal/utils/extra.js";
import { describe } from "self-ref-pkg";
import { alphaFeature } from "self-ref-pkg/feature/alpha";

export function describeInternalAlias(value: string): string {
  const a = internalMarker(value);
  const b = extraMarker(value.length);
  const c = describe(value);
  const d = alphaFeature(value);
  return `${a}|${b}|${c}|${d}`;
}
