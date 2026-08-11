// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export interface AtlasPoint {
  x: number;
  y: number;
}

export function formatPoint(p: AtlasPoint): string {
  return `${p.x},${p.y}`;
}
