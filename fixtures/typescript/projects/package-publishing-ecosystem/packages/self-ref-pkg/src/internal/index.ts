// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export function internalHelper(value: string): string {
  return `internal:${value}`;
}

export interface InternalMarker {
  tag: string;
}
