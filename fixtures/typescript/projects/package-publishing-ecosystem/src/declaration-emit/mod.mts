// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export interface MtsBeacon {
  tag: string;
  kind: "mts";
}

export function describeMts(beacon: MtsBeacon): string {
  return `mts:${beacon.tag}`;
}
