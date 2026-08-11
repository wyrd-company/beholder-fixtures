// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

import type { BeaconCatalogItem } from "./authored-source.js";

// Inferred return type is public-visible even without explicit annotation.
export function buildCatalogLabel(item: BeaconCatalogItem) {
  return `${item.label}::${item.id}`;
}

// Inferred generic public surface.
export function wrapValue<T>(value: T) {
  return { value, kind: "wrapped" as const };
}

export type WrappedCatalog = ReturnType<typeof wrapValue<BeaconCatalogItem>>;
