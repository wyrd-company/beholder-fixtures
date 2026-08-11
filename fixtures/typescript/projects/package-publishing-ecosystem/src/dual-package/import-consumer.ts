// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

import { readDual } from "@fixtures/dual-pkg";
import { readUtils } from "@fixtures/dual-pkg/utils";
import type { BundlerMarker } from "@fixtures/dual-pkg/bundler";
import type { TypesOnlyMarker } from "@fixtures/dual-pkg/types-only";
import { bundlerRead } from "@fixtures/dual-pkg/bundler";

export function describeDualImport(value: string): string {
  const a = readDual(value);
  const b = readUtils(value);
  const c = bundlerRead(value);
  return `${a}|${b}|${c}`;
}

export type ConsumerDualOnly = TypesOnlyMarker;
export type ConsumerBundler = BundlerMarker;
