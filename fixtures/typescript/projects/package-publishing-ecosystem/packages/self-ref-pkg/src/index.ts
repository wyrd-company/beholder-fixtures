// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

import { internalHelper } from "#internal";
import { helperUtil } from "#internal/utils/helper";

export function describe(value: string): string {
  const a = internalHelper(value);
  const b = helperUtil(value.length);
  const c = describeSelf(value);
  return `${a}|${b}|${c}`;
}

export function describeSelf(value: string): string {
  return `self:${value}`;
}

// Re-export via wildcard simulation.
export * from "./feature/alpha.js";
