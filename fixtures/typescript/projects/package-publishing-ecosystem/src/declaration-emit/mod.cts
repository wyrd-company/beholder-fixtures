// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export interface CtsBeacon {
  tag: string;
  kind: "cts";
}

export function describeCts(beacon: CtsBeacon): string {
  return `cts:${beacon.tag}`;
}
