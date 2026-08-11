// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export {};

declare module "flipped-palette" {
  export interface FlippedToneCard {
    revision: number;
  }
}

export type FlippedToneCard = import("flipped-palette").FlippedToneCard;
