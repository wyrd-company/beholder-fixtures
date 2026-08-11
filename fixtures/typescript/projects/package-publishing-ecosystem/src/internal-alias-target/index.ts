// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export function internalMarker(value: string): string {
  return `target:${value}`;
}

export interface InternalTargetMarker {
  marker: "internal-target";
}
