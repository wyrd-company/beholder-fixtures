// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export * from "./namespaces/index.js";
export * from "./ambient-modules/index.js";
export * from "./augmentation/index.js";
export * from "./globals/index.js";
export * from "./triple-slash/index.js";

export function describeFixture(): string {
  return "namespaces-ambient-globals";
}
