// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

import { readMain, type MainBeacon } from "@fixtures/exports-map";
import { formatUtils } from "@fixtures/exports-map/utils";
import { extraUtils } from "@fixtures/exports-map/utils/extra";
import { alphaFeature } from "@fixtures/exports-map/feature/alpha";
import { bundleFeature } from "@fixtures/exports-map/bundle";
import { readViaExports } from "@fixtures/typed-via-exports";

export function describeExportsMap(value: string): string {
  const a = readMain(value);
  const b = formatUtils(value);
  const c = extraUtils(value);
  const d = alphaFeature(value);
  const e = bundleFeature(value);
  const f = readViaExports(value);
  return `${a}|${b}|${c}|${d}|${e}|${f}`;
}

export function createBeacon(id: string): MainBeacon {
  return { id, v5: true } as MainBeacon;
}

// Blocked subpath is not imported — its "null" status is represented by absence.
