// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

import type { HarborChart, HarborSignal } from "./models.js";
import type HarborDefaultBeacon from "../bindings/type-only-default.js";
import { type HarborBuoy, type TideLevel } from "./models.js";
import type * as HarborTypes from "./models.js";

export type BuoyAlias = HarborBuoy;
export type BeaconAlias = HarborDefaultBeacon;
export type ChartAlias = HarborChart;
export type SignalAlias = HarborSignal;

export type TideAlias = TideLevel;
export type ModelsNs = HarborTypes.HarborChart;

export type { HarborChart } from "./models.js";
export type { HarborSignal as HarborSignalRe } from "./models.js";
export type { default as BeaconRe } from "../bindings/type-only-default.js";

export function describeChart(chart: HarborChart): string {
  return `${chart.label}:${chart.depth}`;
}

export function describeBeacon(beacon: HarborDefaultBeacon): number {
  return beacon.intensity;
}
