// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

import { readMain } from "@fixtures/exports-map";
import utils = require("@fixtures/exports-map/utils");
import feature = require("@fixtures/exports-map/feature/alpha");

export function describeRequire(value: string): string {
  const a = readMain(value);
  const b = utils.formatUtils(value);
  const c = feature.alphaFeature(value);
  return `${a}|${b}|${c}`;
}
