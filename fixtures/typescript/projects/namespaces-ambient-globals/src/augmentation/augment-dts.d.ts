// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

import type { RelayCard } from "./base-package/index.js";

declare module "./base-package/index.js" {
  interface RelayCard {
    sourceTag: string;
  }
}

export type RelayCardView = RelayCard;
