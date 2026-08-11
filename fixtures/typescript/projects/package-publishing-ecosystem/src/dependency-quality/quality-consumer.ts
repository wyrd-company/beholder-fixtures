// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

import { readQuality } from "@fixtures/quality-dep/dist/index.js";
import type { QualityMarker } from "@fixtures/quality-dep/dist/index.js";

export function describeQuality(value: string): QualityMarker {
  const result: string = readQuality(value);
  return { kind: "quality", visible: result };
}

// Declaration-versus-runtime mismatch remains invisible to checking:
// readQuality is typed as (string) => string but runtime returns number (42). No diagnostic.
// skipLibCheck on/off is demonstrated by tsconfig.skip-lib-check-on/off.json.
// skipDefaultLibCheck is enabled in the off variant (skipDefaultLibCheck: true) to show lib files are not deeply checked.
