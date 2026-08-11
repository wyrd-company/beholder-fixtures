// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export { AtlasPoint, formatPoint } from "./re-export-chain-a.js";

export interface ShelfMarker {
  tag: string;
  point: import("./re-export-chain-a.js").AtlasPoint;
}
