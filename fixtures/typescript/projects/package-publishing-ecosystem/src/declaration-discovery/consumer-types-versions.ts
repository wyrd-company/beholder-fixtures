// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

import { readVersioned } from "@fixtures/types-versions-pkg";
import type { VersionedMarker } from "@fixtures/types-versions-pkg";

export function describeVersioned(): VersionedMarker {
  return readVersioned();
}
