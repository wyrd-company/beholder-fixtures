// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

// Runtime import(), computed specifier, import("m").T, typeof import("m")

export async function loadTideSignal(): Promise<string> {
  const mod = await import("./target.js");
  return mod.tideSignal;
}

export async function loadComputed(specifier: string): Promise<string> {
  const computed = `./${specifier}.js`;
  const mod = await import(computed);
  return (mod as { tideSignal: string }).tideSignal;
}

export type TideChartType = import("./target.js").TideChart;
export type TideModuleType = typeof import("./target.js");

export async function describeImportType(
  value: TideChartType,
): Promise<string> {
  return `${value.depth}:${value.current}`;
}
