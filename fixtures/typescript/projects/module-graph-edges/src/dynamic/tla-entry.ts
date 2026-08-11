// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

// Top-level await with dependent importer (TS-CAN-022)
export const awaitedTide = await import("./target.js").then(
  (m) => m.tideSignal,
);

export function describeAwaited(): string {
  return awaitedTide;
}
