// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export * from "./bindings/import-matrix.js";
export * from "./bindings/reexport-surface.js";
export * from "./bindings/alias-chain.js";
export * from "./type-only/type-edges.js";
export * from "./type-only/reexports.js";
export * from "./type-only/retention-contrast.js";
export * from "./barrel/barrel.js";
export * from "./barrel/cyclic-a.js";
export * from "./barrel/cyclic-b.js";
export * from "./side-effects/bare-consumer.js";
export * from "./side-effects/asset-consumer.js";
export * from "./side-effects/patch-consumer.js";
export * from "./dynamic/dynamic-consumer.js";
export * from "./dynamic/import-type-consumer.js";
export * from "./dynamic/meta-consumer.js";
export * from "./dynamic/tla-entry.js";
export * from "./dynamic/tla-dependent.js";

export function describeFixture(): string {
  return "module-graph-edges";
}
