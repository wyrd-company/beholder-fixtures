// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export * from "./control-flow/index.js";
export * from "./predicates/index.js";
export * from "./contextual/index.js";
export * from "./assertions/index.js";

export function describeFixture(): string {
  return "narrowing-inference-assertions";
}
