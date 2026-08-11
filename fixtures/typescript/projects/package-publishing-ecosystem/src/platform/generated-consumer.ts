// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

import type { AtlasPoint, ShelfMarker } from "../../generated/rolled.js";
import { describeGeneratedPlatform } from "../../generated/platform-generated/index.js";
import type { PlatformGeneratedMarker } from "../../generated/platform-generated/index.js";

export function describeRolled(point: AtlasPoint): ShelfMarker {
  return { tag: "rolled", point };
}

export function describeGenerated(
  platform: PlatformGeneratedMarker["platform"],
): string {
  return describeGeneratedPlatform(platform);
}
