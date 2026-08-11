// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

import { readRelay, type RelayCard } from "./base-package/index.js";

export function describeRelayWithoutAugmentation(card: RelayCard): string {
  return readRelay(card);
}
