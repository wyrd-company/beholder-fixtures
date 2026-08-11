// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export { harborName as harborLabel } from "./origins.js";

// Type/value alias chain: HarborSkiff is both a value (class) and a type.
export { HarborSkiff as HarborVessel } from "./origins.js";

// Single alias that carries both type and value meanings
import { HarborSkiff } from "./origins.js";

export { HarborSkiff };

export type HarborSkiffType = HarborSkiff;
export const harborSkiffValue: HarborSkiff = new HarborSkiff("chain-1");

export function useAliasBoth(): { asType: HarborSkiff; asValue: string } {
  const vessel: HarborSkiff = harborSkiffValue;
  return { asType: vessel, asValue: vessel.moor() };
}
