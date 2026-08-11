// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

import { valueFromB } from "./cyclic-b.js";

export const valueFromA = "alpha";

export async function getFromA(): Promise<string> {
  const fromB = await Promise.resolve(valueFromB);
  return `a:${valueFromA}:b:${fromB}`;
}
