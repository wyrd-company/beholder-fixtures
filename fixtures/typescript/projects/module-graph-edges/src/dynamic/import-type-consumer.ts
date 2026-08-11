// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

// Import-type with resolution-mode (TS-CAN-022)

export type TideChartImport = import("./target.js", {
  with: { "resolution-mode": "import" },
}).TideChart;

export type TideSignalRequire = import("./target.js", {
  with: { "resolution-mode": "require" },
}).TideChart;
