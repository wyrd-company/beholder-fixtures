// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

import { valueFromA } from "./cyclic-a.js";

export const valueFromB = "beta";

export async function getFromB(): Promise<string> {
  const fromA = await Promise.resolve(valueFromA);
  return `b:${valueFromB}:a:${fromA}`;
}
