// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

declare module "exact-palette" {
  export const hue: number;
  export default function readHue(): number;
}

declare module "equals-palette" {
  export function readTone(): string;
  export = readTone;
}

declare module "pattern-slot-*" {
  export const slotId: string;
}

declare module "shorthand-slot";

declare module "flipped-palette" {
  export interface FlippedToneCard {
    tone: string;
  }
}

declare module "unmatched-ledger" {
  export const ledgerId: string;
}
