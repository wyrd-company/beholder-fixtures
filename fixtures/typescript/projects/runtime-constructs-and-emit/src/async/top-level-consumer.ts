// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

import { topLevelValue } from "./top-level-await.js";

export async function consumeTopLevel(): Promise<string> {
  return `consumed:${topLevelValue}`;
}

export function describeTopLevel(): string {
  return `top:${topLevelValue}`;
}
