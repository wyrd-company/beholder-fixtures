// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

import type { QualityMarker as DepQuality } from "@fixtures/quality-dep/dist/index.js";

export interface LocalQuality {
  kind: "quality";
  visible: string;
  local: true;
}

export type CombinedQuality = DepQuality | LocalQuality;

export function mergeQuality(
  dep: DepQuality,
  local: LocalQuality,
): CombinedQuality {
  return dep.visible.length > local.visible.length ? dep : local;
}

// Local .d.ts (this file) versus dependency .d.ts demonstrates local versus dependency declaration provenance.
