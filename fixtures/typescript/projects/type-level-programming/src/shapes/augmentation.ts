// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

import type { OrchardPayload } from "./interface-alias.js";

// TS-CAN-075: module augmentation

declare module "./interface-alias.js" {
  interface AtlasInterface {
    augmented?: boolean;
  }
}

export type AugmentedAtlas = {
  label: string;
  count: number;
  tag: string;
  augmented: boolean;
};

export const augmentedExample: AugmentedAtlas = {
  label: "atlas",
  count: 3,
  tag: "beacon",
  augmented: true,
};

export function describePayload(payload: OrchardPayload): string {
  return `${payload.label}:${payload.count}`;
}
