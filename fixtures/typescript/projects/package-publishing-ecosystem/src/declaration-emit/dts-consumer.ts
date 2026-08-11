// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

// Consumes .d.ts independently from runtime code — types only.
import type { StandaloneBeacon } from "./standalone.js";
import type { BeaconCatalogItem } from "./authored-source.js";

export function describeStandalone(beacon: StandaloneBeacon): string {
  return `standalone:${beacon.beaconId}:${beacon.revision}`;
}

export function promoteCatalog(item: BeaconCatalogItem): StandaloneBeacon {
  return { beaconId: item.id, revision: item.label.length };
}

// Navigation back to authored sources is via declarationMap (verified by emit).
export type ConsumerExposed = BeaconCatalogItem & StandaloneBeacon;
