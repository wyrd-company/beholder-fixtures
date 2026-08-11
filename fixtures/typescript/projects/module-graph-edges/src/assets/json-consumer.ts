// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

// JSON import with typed valid property and with { type: "json" } attribute
// (TS-CAN-023) — requires resolveJsonModule and modern attribute syntax.
import harborData from "./data.json" with { type: "json" };

export function describeJson(): string {
  const valid: string = harborData.harbor;
  const depth: number = harborData.depth;
  return `${valid}:${depth}`;
}
