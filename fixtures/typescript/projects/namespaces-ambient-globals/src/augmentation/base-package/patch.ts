// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

import { RelayCard } from "./index.js";

RelayCard.format = (card) => `patched:${card.channel}:${card.revision}`;

export {};
