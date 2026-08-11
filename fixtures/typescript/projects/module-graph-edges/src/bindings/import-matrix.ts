// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

// Import binding matrix (TS-CAN-018): named, renamed, default, namespace, side-effect

import { harborName } from "./origins.js";
import { harborName as harborRenamed } from "./origins.js";
import HarborSkiffDefault from "./origins.js";
import * as HarborAll from "./origins.js";
import "./origins.js";

import { harborLabel } from "./alias-chain.js";

export function describeImports(): string[] {
  const v = new HarborSkiffDefault("matrix-1");
  return [
    harborName,
    harborRenamed,
    v.moor(),
    HarborAll.harborCount.toString(),
    harborLabel,
  ];
}

export { harborName, harborRenamed, HarborSkiffDefault, HarborAll };
