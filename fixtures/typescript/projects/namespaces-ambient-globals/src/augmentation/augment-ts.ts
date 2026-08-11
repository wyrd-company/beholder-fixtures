// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

import { RelayCard } from "./base-package/index.js";

declare module "./base-package/index.js" {
  interface RelayCard {
    revision: number;
  }
}

export function describeAugmentedRelay(card: RelayCard): {
  channel: string;
  revision: number;
  formatted: string;
} {
  return {
    channel: card.channel,
    revision: card.revision,
    formatted: RelayCard.format(card),
  };
}

declare global {
  interface RelayGlobalMarker {
    relayScope: "module-augment";
  }
}

export function readRelayGlobal(): RelayGlobalMarker {
  return { relayScope: "module-augment" };
}
