// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

// Imported and exported string-named bindings (TS-CAN-023)

import { "harbor beacon" as beaconAlias } from "./arbitrary-origin.js";
export { "harbor beacon" as "exported beacon" } from "./arbitrary-origin.js";
export type { "Harbor Chart" as HarborChartRe } from "./arbitrary-origin.js";

export function describeArbitrary(): string {
  return beaconAlias;
}
