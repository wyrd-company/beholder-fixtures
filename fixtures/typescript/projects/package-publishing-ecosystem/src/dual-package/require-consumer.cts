// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

import { readDual } from "@fixtures/dual-pkg";
import utils = require("@fixtures/dual-pkg/utils");

export function describeDualRequire(value: string): string {
  const a = readDual(value);
  const b = utils.readUtils(value);
  return `${a}|${b}`;
}
