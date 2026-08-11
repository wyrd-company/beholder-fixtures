// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export const tideSignal = "tide-signal";
export type TideChart = { depth: number; current: string };
export function readTide(): string {
  return tideSignal;
}

export interface ImportMetaFixture {
  harbor: string;
}
