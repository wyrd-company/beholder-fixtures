// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export * from "./conditional/index.js";
export * from "./mapped/index.js";
export * from "./keyof/index.js";
export * from "./template/index.js";
export * from "./recursive/index.js";
export * from "./shapes/index.js";
export * from "./utilities/index.js";

export function describeFixture(): string {
  return "type-level-programming";
}
