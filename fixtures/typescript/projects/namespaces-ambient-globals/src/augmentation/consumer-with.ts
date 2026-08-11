// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

import "./base-package/patch.js";
import { readRelay, type RelayCard } from "./base-package/index.js";
import { describeAugmentedRelay } from "./augment-ts.js";
import type { RelayCardView } from "./augment-dts.d.ts";

export function describeRelayWithAugmentation(): {
  raw: string;
  augmented: ReturnType<typeof describeAugmentedRelay>;
  dtsView: RelayCardView["sourceTag"];
} {
  const card: RelayCard = { channel: "alpha", revision: 2, sourceTag: "dts" };
  const raw = readRelay(card);
  const augmented = describeAugmentedRelay(card);
  const dtsView: RelayCardView["sourceTag"] = card.sourceTag;

  return { raw, augmented, dtsView };
}
